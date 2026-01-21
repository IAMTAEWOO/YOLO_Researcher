import time
import csv
from datetime import datetime
from pathlib import Path

import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
from gpiozero import (
    MotionSensor,
    LED,
    Buzzer,
    DistanceSensor,
    Servo,
    Button,
)

# ── 핀/설정 ─────────────────────────────────────────────
PIR_PIN = 17
LED_PIN = 27
BUZZER_PIN = 22

US_TRIG_PIN = 23
US_ECHO_PIN = 24

SERVO_PIN = 18
BUTTON_PIN = 5

IMG_W, IMG_H = 1280, 720
CONF_THRES = 0.3
IOU_THRES = 0.5

# 전처리 파라미터
BRIGHTNESS = 1.2
SATURATION = 1.5
CONTRAST = 1.2

# 라벨 우선순위
PERSON_LABELS = {"person"}
OBJECT_LABELS = {
    "bottle",
    "cup",
    "laptop",
    "cell phone",
    "chair",
    "book",
}

LOG_PATH = Path("events_ultra_pir_servo.csv")
IMG_SAVE_PATH = Path("last_detect_ultra_pir_servo.jpg")

# 초음파 감지 임계값 (m)
ULTRA_THRESHOLD = 0.6

# 서보 설정
SERVO_CLOSED_POS = -0.8
SERVO_OPEN_POS = 0.0
SERVO_HOLD_TIME = 5.0


# ── 유틸 함수 ──────────────────────────────────────────
def init_camera():
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (IMG_W, IMG_H)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.preview_configuration.align()
    picam2.configure("preview")
    picam2.start()
    time.sleep(0.5)
    return picam2


def capture_rgb_frame(picam2):
    return picam2.capture_array()


def init_logger(path: Path):
    new_file = not path.exists()
    f = path.open("a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["timestamp", "trigger", "labels", "count", "note"])
    return f, writer


def beep_times(buzzer, n=3, on=0.1, off=0.1):
    for _ in range(n):
        buzzer.on()
        time.sleep(on)
        buzzer.off()
        time.sleep(off)


def servo_move_and_detach(servo, pos, move_time=0.8):
    servo.value = pos
    time.sleep(move_time)
    servo.value = None


# ── 메인 ───────────────────────────────────────────────
def main():
    pir = MotionSensor(PIR_PIN)
    led = LED(LED_PIN)
    buzzer = Buzzer(BUZZER_PIN)

    ultra = DistanceSensor(
        echo=US_ECHO_PIN,
        trigger=US_TRIG_PIN,
        max_distance=2.0,
    )

    servo = Servo(
        SERVO_PIN,
        min_pulse_width=0.6 / 1000.0,
        max_pulse_width=2.4 / 1000.0,
    )

    button = Button(BUTTON_PIN, pull_up=True)

    servo_move_and_detach(servo, SERVO_CLOSED_POS)

    picam2 = init_camera()
    model = YOLO("yolov8n.pt")

    log_file, writer = init_logger(LOG_PATH)

    prev_pir_motion = False
    prev_ultra_trigger = False
    led_mode = "off"
    led_state = False
    last_led_toggle_time = 0.0

    servo_mode = "idle"
    servo_last_change = 0.0

    PERSON_BLINK_INTERVAL = 0.5
    OBJECT_BLINK_INTERVAL = 0.25

    try:
        while True:
            now = time.time()

            pir_motion = pir.motion_detected
            try:
                dist = ultra.distance
            except Exception:
                dist = 10.0

            ultra_trigger = dist < ULTRA_THRESHOLD

            ultra_edge = ultra_trigger and not prev_ultra_trigger
            pir_edge = pir_motion and not prev_pir_motion

            trigger_type = None
            if ultra_edge:
                trigger_type = "ultrasonic"
            elif pir_edge:
                trigger_type = "pir"

            if trigger_type:
                frame_rgb = capture_rgb_frame(picam2)
                results = model.predict(
                    frame_rgb,
                    imgsz=IMG_W,
                    conf=CONF_THRES,
                    iou=IOU_THRES,
                    verbose=False,
                )
                r = results[0]

                labels = []
                if r.boxes is not None:
                    for cls in r.boxes.cls.int().tolist():
                        labels.append(r.names[int(cls)])

                label_set = set(labels)

                if label_set & PERSON_LABELS:
                    led_mode = "person"
                    beep_times(buzzer)
                elif label_set & OBJECT_LABELS:
                    led_mode = "object"
                else:
                    led_mode = "off"
                    led.off()
                    led_state = False

                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    trigger_type,
                    "|".join(label_set) if label_set else "none",
                    len(labels),
                    led_mode,
                ])
                log_file.flush()

                annotated = r.plot()
                cv2.imwrite(str(IMG_SAVE_PATH), annotated)
                last_led_toggle_time = now

            if led_mode in ("person", "object"):
                interval = (
                    PERSON_BLINK_INTERVAL
                    if led_mode == "person"
                    else OBJECT_BLINK_INTERVAL
                )
                if now - last_led_toggle_time >= interval:
                    led_state = not led_state
                    led.value = led_state
                    last_led_toggle_time = now
            else:
                led.off()
                led_state = False

            if led_mode == "person" and button.is_pressed and servo_mode == "idle":
                servo_move_and_detach(servo, SERVO_OPEN_POS)
                servo_mode = "open_hold"
                servo_last_change = now

            if servo_mode == "open_hold" and now - servo_last_change >= SERVO_HOLD_TIME:
                servo_move_and_detach(servo, SERVO_CLOSED_POS)
                servo_mode = "idle"

            prev_pir_motion = pir_motion
            prev_ultra_trigger = ultra_trigger

            time.sleep(0.01)

    except KeyboardInterrupt:
        pass
    finally:
        led.off()
        buzzer.off()
        servo_move_and_detach(servo, SERVO_CLOSED_POS)
        picam2.stop()
        log_file.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

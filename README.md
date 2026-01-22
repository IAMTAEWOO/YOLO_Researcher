# Multi-Sensor Vision-Based Secure Door System

본 프로젝트는 Raspberry Pi 5를 기반으로 카메라, PIR 센서, 초음파 센서를 융합하여
객체 및 사람을 인식하고, 조건이 만족될 경우 서보 모터를 통해 보안 도어를 제어하는
지능형 보안 시스템이다.

YOLOv8 객체 인식 모델과 다중 센서 트리거를 결합하여
오탐을 줄이고 실제 상황에 적합한 접근 제어를 구현하였다.

---

## System Overview

### Sensors
- Camera (Picamera2): 객체 및 사람 인식
- PIR Motion Sensor: 움직임 감지
- Ultrasonic Sensor (HC-SR04): 근접 거리 감지

### Actuators
- Servo Motor: 도어 개폐 제어
- LED: 상태 시각화
- Buzzer: 경고 알림

### Control Logic
1. 초음파 또는 PIR 센서 감지 발생
2. 카메라 캡처 및 YOLO 객체 인식 수행
3. 사람이 감지된 경우 LED 점등 및 부저 경고
4. 버튼 입력 시 서보 모터를 통해 도어 개방
5. 일정 시간 후 자동으로 도어 닫힘

---

## Hardware Configuration

- Raspberry Pi 5
- Picamera2
- PIR Motion Sensor
- Ultrasonic Sensor (HC-SR04)
- Servo Motor
- LED
- Buzzer
- Push Button

모든 GPIO는 3.3V 기준으로 구성하였다.

---

## Software Stack

- Python 3
- OpenCV
- Ultralytics YOLOv8
- gpiozero
- Picamera2

---

## Running the System

```bash
pip install -r requirements.txt
python src/main.py

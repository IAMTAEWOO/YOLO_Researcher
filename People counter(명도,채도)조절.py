import cv2
from ultralytics import YOLO

# YOLOv8 모델 로드
model = YOLO("yolov8n.pt")

# 이미지 파일 경로 설정
image_path = "5.JPEG"

# 이미지 읽기
image = cv2.imread(image_path)

# === 밝기와 채도 조절 함수 ===
def adjust_brightness_saturation(image, brightness=1.0, saturation=1.0):
    # BGR 이미지를 HSV로 변환
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # 명도(V) 조절
    v = cv2.multiply(v, brightness)
    v = cv2.min(v, 255)  # 값이 255를 초과하지 않도록 제한

    # 채도(S) 조절
    s = cv2.multiply(s, saturation)
    s = cv2.min(s, 255)  # 값이 255를 초과하지 않도록 제한

    # 채널 병합 및 BGR로 다시 변환
    hsv_adjusted = cv2.merge([h, s, v])
    adjusted_image = cv2.cvtColor(hsv_adjusted, cv2.COLOR_HSV2BGR)

    return adjusted_image

# === 조정 값 설정 ===
brightness = 1.2  # 밝기
saturation = 1.2  # 채도

# 밝기와 채도 조절 적용
adjusted_image = adjust_brightness_saturation(image, brightness=brightness, saturation=saturation)

# === YOLO로 객체 감지 수행 ===
results = model(adjusted_image, conf=0.1)

# "person" 클래스만 필터링 (COCO 데이터셋에서 "person"의 클래스 ID는 0)
person_detections = [d for d in results[0].boxes if d.cls == 0]

# 감지된 사람 수
person_count = len(person_detections)

# 감지된 결과를 이미지에 시각화
annotated_image = results[0].plot()

# 감지된 사람 수 출력
print(f"Number of people detected: {person_count}")

# 이미지에 사람 수 표시
text = f"People count: {person_count}"
font = cv2.FONT_HERSHEY_SIMPLEX
text_size = cv2.getTextSize(text, font, 1, 2)[0]
text_x = 10
text_y = text_size[1] + 10
cv2.putText(annotated_image, text, (text_x, text_y), font, 1, (255, 255, 255), 2)

# 결과 이미지 보기
cv2.imshow("People Counter", annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 결과 이미지 저장
cv2.imwrite("annotated_image.jpg", annotated_image)

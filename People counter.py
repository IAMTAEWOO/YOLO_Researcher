import cv2
from ultralytics import YOLO

# YOLOv8 모델 로드 (사람만 감지하도록 사전 학습된 모델 사용 가능)
model = YOLO("yolov8n.pt")  # 필요시 경량화된 모델 사용

# 이미지 파일 경로 설정
image_path = "5.JPEG"

# 이미지 읽기
image = cv2.imread(image_path)

# YOLO로 객체 감지 수행
results = model(image, conf=0.25)  # 신뢰도 임계값(conf)을 조정 가능

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
cv2.waitKey(0)  # 키 입력 대기
cv2.destroyAllWindows()

# 결과 이미지 저장
cv2.imwrite("pc.jpg", annotated_image)

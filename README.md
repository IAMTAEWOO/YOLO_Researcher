# YOLO_Researcher
undergraduate researcher's Project about YOLO

# 스마트 보안 카메라 (PIR + 초음파 + YOLO)

Raspberry Pi에서 PIR 센서와 초음파 센서로 **사람/물건을 감지**하고 **YOLOv8**으로 인식하여 LED 점멸과 서보모터로 반응하는 보안 시스템입니다.

![시스템 개요](last_detect_ultra_pir_servo.jpg)

## 🎯 주요 기능

- **PIR 센서**: 인간 움직임 감지
- **초음파 센서**: 60cm 이내 물건 접근 감지  
- **YOLOv8**: 실시간 사람/물건 인식 (bottle, cup, laptop 등 7종)
- **RGB 카메라**: 감지시 자동 사진 촬영
- **서보모터**: 사람 감지 + 버튼 → 문/창문 자동 개폐
- **LED**: 사람(느린 깜빡임)/물건(빠른 깜빡임) 구분 표시
- **CSV 로깅**: 모든 감지 이벤트 기록

## 🛠️ 하드웨어 요구사항

```
Raspberry Pi 4/5 (카메라 모듈 필수)
├─ PIR 센서 (핀 17)
├─ 초음파 센서 (Trig 23, Echo 24)  
├─ LED (핀 27)
├─ 부저 (핀 22)
├─ 서보모터 (핀 18)
└─ 버튼 (핀 5, 풀업)
```

## 📦 설치 및 실행

```bash
# 의존성 설치
pip install ultralytics opencv-python picamera2 gpiozero

# YOLO 모델 자동 다운로드 (yolov8n.pt)
python main.py
```

**Ctrl+C**로 안전 종료됩니다.

## 📊 출력 파일

```
events_ultra_pir_servo.csv     # 감지 로그
last_detect_ultra_pir_servo.jpg # 최종 감지 이미지
```

**CSV 형식**: `timestamp | trigger | labels | count | note`

## 🎮 사용법

1. **자동 감지**: PIR/초음파가 사람/물건을 감지
2. **사람 확인**: LED 느린 깜빡임 + 부저 3회
3. **버튼 누름**: 서보 5초간 열림 → 자동 닫힘

## ⚙️ 설정값 조정

```python
CONF_THRES = 0.3        # YOLO 신뢰도
ULTRA_THRESHOLD = 0.6   # 초음파 감지 거리(m)
SERVO_HOLD_TIME = 5.0   # 서보 열림 시간(초)
```

## 🔧 문제 해결

- **카메라 오류**: `sudo raspi-config` → Camera 활성화
- **GPIO 권한**: `sudo usermod -a -G gpio $USER`
- **YOLO 느림**: `yolov8n.pt` → `yolov8s.pt`로 변경

## 📄 라이선스

MIT License

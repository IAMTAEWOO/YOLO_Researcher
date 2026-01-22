# System Control Flow

1. System initializes all sensors and actuators
2. Ultrasonic sensor monitors proximity continuously
3. PIR sensor monitors motion events
4. On trigger edge:
   - Capture camera frame
   - Perform YOLO object detection
5. Detection result handling:
   - Person detected → LED + Buzzer
   - Object detected → LED only
6. If person detected and button pressed:
   - Open door using servo motor
   - Hold open state for fixed duration
7. Door automatically closes after timeout

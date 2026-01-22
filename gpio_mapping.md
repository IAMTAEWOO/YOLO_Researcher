# GPIO Mapping

| Component        | GPIO Pin |
|------------------|----------|
| PIR Sensor       | GPIO 17  |
| LED              | GPIO 27  |
| Buzzer           | GPIO 22  |
| Ultrasonic TRIG  | GPIO 23  |
| Ultrasonic ECHO  | GPIO 24  |
| Servo Motor      | GPIO 18  |
| Button           | GPIO 5   |

## Power Configuration
- GPIO logic level: 3.3V
- Sensors & Actuators:
  - PIR sensor: 5V
  - Ultrasonic sensor (HC-SR04): 5V
  - Servo motor: 5V
- Camera and control signals operate at 3.3V

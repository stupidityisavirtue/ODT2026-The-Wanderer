# Individual Codes and works
import machine
import time
import network
import espnow

SERVO_PINS = [0, 3, 4, 6]
MIN_PULSE = 1000
MAX_PULSE = 2000
FREQ = 50

def map_value_to_pulse(value):
    return int(MIN_PULSE + (MAX_PULSE - MIN_PULSE) * (value / 100))

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

en = espnow.ESPNow()
en.active(True)

servos = []
for pin_num in SERVO_PINS:
    servo = machine.PWM(machine.Pin(pin_num), freq=FREQ)
    servo.duty(map_value_to_pulse(50))
    servos.append(servo)

def move_pair(indices, low=30, high=70):
    for i in indices:
        servos[i].duty(map_value_to_pulse(low))
    time.sleep_ms(150)

    for i in indices:
        servos[i].duty(map_value_to_pulse(high))
    time.sleep_ms(150)

    for i in indices:
        servos[i].duty(map_value_to_pulse(50))

while True:
    host, msg = en.recv()

    if msg:
        try:
            command = msg.decode().strip()
            print("Received:", command)

            if command == "L":
                move_pair([2, 1])   # left arm + right leg

            elif command == "R":
                move_pair([3, 0])   # right arm + left leg

            elif command == "U":
                move_pair([0, 1])   # both legs

            elif command == "D":
                move_pair([2, 3], 10, 90)   # both arms bigger motion

            elif command == "S":
                for s in servos:
                    s.duty(map_value_to_pulse(50))

        except Exception as e:
            print("Error:", e)

    time.sleep_ms(20)

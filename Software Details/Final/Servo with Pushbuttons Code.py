from machine import Pin, I2C
from pca9685 import PCA9685
import time


i2c = I2C(0, scl=Pin(19), sda=Pin(18))
pwm = PCA9685(i2c)
pwm.set_pwm_freq(50)

btn1 = Pin(22, Pin.IN, Pin.PULL_UP)
btn2 = Pin(23, Pin.IN, Pin.PULL_UP)
btn3 = Pin(32, Pin.IN, Pin.PULL_UP)


buzzer = Pin(27, Pin.OUT)


servo0 = 0
servo3 = 3
servo4 = 4
servo6 = 6


angles = {
    0: 0,
    3: 0,
    4: 0,
    6: 0
}


def angle_to_pulse(angle):
    min_pulse = 150
    max_pulse = 600
    return int(min_pulse + (angle / 180) * (max_pulse - min_pulse))

# Move servo
def move_servo(ch):
    angles[ch] += 45
    if angles[ch] > 180:
        angles[ch] = 0

    pulse = angle_to_pulse(angles[ch])
    pwm.set_pwm(ch, 0, pulse)

# Beep
def beep():
    buzzer.value(1)
    time.sleep_ms(100)
    buzzer.value(0)


def pressed(btn):
    if btn.value() == 0:
        time.sleep_ms(20)
        if btn.value() == 0:
            return True
    return False

print("System Ready 🚀")

while True:

 
    if pressed(btn1):
        beep()
        move_servo(servo0)
        move_servo(servo3)
        time.sleep_ms(250)


    if pressed(btn2):
        beep()
        move_servo(servo4)
        move_servo(servo6)
        time.sleep_ms(250)

    
    if pressed(btn3):
        beep()
        move_servo(servo0)
        move_servo(servo4)
        time.sleep_ms(250)
#servo with pushbutton code 
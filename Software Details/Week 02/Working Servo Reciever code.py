import network
import espnow
from machine import I2C, Pin
import time
from pca9685 import PCA9685


i2c = I2C(0, scl=Pin(22), sda=Pin(21))
pca = PCA9685(i2c)
pca.freq(50)


LEFT_LEG  = 0
RIGHT_LEG = 3
LEFT_ARM  = 4
RIGHT_ARM = 6
#(what is movement AHHHHH)

def set_servo(ch, angle):
    duty = int(40 + (angle / 180) * 75)
    pca.duty(ch, duty)

def move(channels, a=60, b=120):
    for ch in channels:
        set_servo(ch, a)
    time.sleep(0.15)
    for ch in channels:
        set_servo(ch, b)
    time.sleep(0.15)
    for ch in channels:
        set_servo(ch, 90)

# --- INIT POSITION ---
for ch in [LEFT_LEG, RIGHT_LEG, LEFT_ARM, RIGHT_ARM]:
    set_servo(ch, 90)

# --- ESP NOW ---
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

print("Receiver Ready")


while True:
    host, msg = e.recv()

    if msg:

        # RIGHT → right arm + left leg
        if msg == b'R':
            move([RIGHT_ARM, LEFT_LEG])

        # LEFT → left arm + right leg
        elif msg == b'L':
            move([LEFT_ARM, RIGHT_LEG])

        # UP → both legs
        elif msg == b'U':
            move([LEFT_LEG, RIGHT_LEG])

        # DOWN → both arms (bigger swing)
        elif msg == b'D':
            move([LEFT_ARM, RIGHT_ARM], 30, 150)

        # STOP
        elif msg == b'S':
            for ch in [LEFT_LEG, RIGHT_LEG, LEFT_ARM, RIGHT_ARM]:
                set_servo(ch, 90)
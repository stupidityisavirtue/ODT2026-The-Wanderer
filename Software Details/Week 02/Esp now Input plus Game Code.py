#Esp now Integration Input code?

import machine
import time
import random
import framebuf
import sh1106
import ssd1306
import network
import espnow
import idle, up, down, left, right, error

SCL_PIN = 18
SDA_PIN = 19

SSD1306_SCL = 22
SSD1306_SDA = 23

right_button = 27
down_button  = 14
up_button    = 32
left_button  = 13

start_button = 25
stop_button  = 26

LANE_WIDTH = 24
HIT_LINE_Y = 43
GOOD_WINDOW = 250

DEBOUNCE_MS = 200

sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)

peer = b'\xc0\xcd\xd6\x84\x9a\x60'
e.add_peer(peer)

i2c0 = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN))
display = sh1106.SH1106_I2C(128, 64, i2c0)

i2c1 = machine.I2C(1, scl=machine.Pin(SSD1306_SCL), sda=machine.Pin(SSD1306_SDA))
anim_display = ssd1306.SSD1306_I2C(128, 64, i2c1)

anim_buffer = bytearray(128 * 8)
anim_fb = framebuf.FrameBuffer(anim_buffer, 128, 64, framebuf.MONO_VLSB)

pins = [
    machine.Pin(right_button, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(down_button,  machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(up_button,    machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(left_button,  machine.Pin.IN, machine.Pin.PULL_UP)
]

start_pin = machine.Pin(start_button, machine.Pin.IN, machine.Pin.PULL_UP)
stop_pin  = machine.Pin(stop_button,  machine.Pin.IN, machine.Pin.PULL_UP)

arrow_left  = bytearray([0x18,0x3C,0x7E,0x18,0x18,0x18,0x00,0x00])
arrow_right = bytearray([0x18,0x18,0x18,0x7E,0x3C,0x18,0x00,0x00])
arrow_up    = bytearray([0x10,0x18,0x1C,0xFE,0x1C,0x18,0x10,0x00])
arrow_down  = bytearray([0x08,0x18,0x38,0xFE,0x38,0x18,0x08,0x00])

def draw_arrow(x, y, direction):
    if direction == "up":
        fb = framebuf.FrameBuffer(arrow_up, 8, 8, framebuf.MONO_VLSB)
    elif direction == "down":
        fb = framebuf.FrameBuffer(arrow_down, 8, 8, framebuf.MONO_VLSB)
    elif direction == "left":
        fb = framebuf.FrameBuffer(arrow_left, 8, 8, framebuf.MONO_VLSB)
    else:
        fb = framebuf.FrameBuffer(arrow_right, 8, 8, framebuf.MONO_VLSB)
    display.blit(fb, x-4, y-4)

def update_anim(state):
    if state == "up":
        data = up.bitmap_data
    elif state == "down":
        data = down.bitmap_data
    elif state == "left":
        data = left.bitmap_data
    elif state == "right":
        data = right.bitmap_data
    elif state == "error":
        data = error.bitmap_data
    else:
        data = idle.bitmap_data

    anim_display.fill(0)
    temp = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    anim_display.blit(temp, 0, 0)
    anim_display.show()

def generate_notes():
    notes = []
    t = 2000
    for _ in range(50):
        t += 2000
        notes.append({
            "time": t,
            "lane": random.randint(0, 3),
            "hit": False,
            "passed": False
        })
    return notes

def is_pressed(pin, last_time):
    now = time.ticks_ms()
    if not pin.value() and time.ticks_diff(now, last_time) > DEBOUNCE_MS:
        return True, now
    return False, last_time

def main():
    combo = 0
    errors = 0
    last_hit_time = 0
    last_btn_states = [False]*4
    anim_state = "idle"

    running = False
    start_time = time.ticks_ms()
    notes = []

    last_start_time = 0
    last_stop_time  = 0

    display.fill(0)
    display.text("PRESS START", 10, 25, 1)
    display.show()
    update_anim("idle")

    while True:

        stop_fired, last_stop_time = is_pressed(stop_pin, last_stop_time)
        if stop_fired:
            running = False
            e.send(peer, b'S')

            display.fill(0)
            display.text("STOPPED", 30, 25, 1)
            display.show()
            time.sleep_ms(500)

            display.fill(0)
            display.show()
            anim_display.fill(0)
            anim_display.show()

        start_fired, last_start_time = is_pressed(start_pin, last_start_time)
        if start_fired and not running:
            running = True
            e.send(peer, b'X')

            combo = 0
            errors = 0
            last_hit_time = 0
            last_btn_states = [False]*4
            notes = generate_notes()

            start_time = time.ticks_ms()

            display.fill(0)
            display.text("START", 45, 25, 1)
            display.show()
            time.sleep_ms(300)

            update_anim("idle")

        if not running:
            time.sleep_ms(20)
            continue

        now = time.ticks_diff(time.ticks_ms(), start_time)

        display.fill(0)

        for i in range(5):
            display.vline(i * LANE_WIDTH, 0, 64, 1)
        display.hline(0, HIT_LINE_Y, LANE_WIDTH * 4, 1)

        current = [not p.value() for p in pins]
        pressed = [False]*4

        for i in range(4):
            if current[i] and not last_btn_states[i]:
                pressed[i] = True

        last_btn_states = current

        if pressed[0]:
            anim_state = "right"
            last_hit_time = now
            e.send(peer, b'R')

        elif pressed[1]:
            anim_state = "down"
            last_hit_time = now
            e.send(peer, b'D')

        elif pressed[2]:
            anim_state = "up"
            last_hit_time = now
            e.send(peer, b'U')

        elif pressed[3]:
            anim_state = "left"
            last_hit_time = now
            e.send(peer, b'L')

        if now - last_hit_time > 1000:
            anim_state = "idle"

        for note in notes:
            if note["hit"] or note["passed"]:
                continue

            dist = note["time"] - now
            y = int(HIT_LINE_Y - (dist / 30))
            lane = note["lane"]
            direction = ["right","down","up","left"][lane]

            if -10 < y < 64:
                x = lane * LANE_WIDTH + (LANE_WIDTH // 2)
                draw_arrow(x, y, direction)

            if abs(dist) < GOOD_WINDOW:
                if pressed[lane]:
                    note["hit"] = True
                    combo += 1
                    last_hit_time = now
                    pressed[lane] = False

            elif dist < -GOOD_WINDOW:
                note["passed"] = True
                errors += 1
                last_hit_time = now
                anim_state = "error"

        update_anim(anim_state)

        display.text("E:{}".format(errors), 98, 30, 1)
        display.text("C:{}".format(combo), 98, 50, 1)

        display.show()
        time.sleep_ms(5)

main()


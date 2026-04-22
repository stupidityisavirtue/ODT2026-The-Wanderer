from machine import Pin, I2C
import ssd1306
import time

# ─── OLED SETUP ─────────────────────
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ─── BUTTONS ────────────────────────
btn_up    = Pin(12, Pin.IN, Pin.PULL_UP)
btn_left  = Pin(14, Pin.IN, Pin.PULL_UP)
btn_down  = Pin(27, Pin.IN, Pin.PULL_UP)
btn_right = Pin(32, Pin.IN, Pin.PULL_UP)

# ─── CENTER POSITION ────────────────
cx = 64
cy = 32
size = 6

# current position
x = cx
y = cy

# how far it moves
offset = 12

# ─── INPUT ──────────────────────────
def read_buttons():
    return {
        "UP":    not btn_up.value(),
        "LEFT":  not btn_left.value(),
        "DOWN":  not btn_down.value(),
        "RIGHT": not btn_right.value()
    }

# ─── LOOP ───────────────────────────
while True:
    buttons = read_buttons()

    # reset to center every frame
    x = cx
    y = cy

    # apply movement
    if buttons["UP"]:
        y = cy - offset
    elif buttons["DOWN"]:
        y = cy + offset
    elif buttons["LEFT"]:
        x = cx - offset
    elif buttons["RIGHT"]:
        x = cx + offset

    # DRAW
    oled.fill(0)
    oled.fill_rect(int(x), int(y), size, size, 1)

    # center reference (optional, remove if annoying)
    # oled.pixel(cx, cy, 1)

    oled.show()

    time.sleep(0.03)

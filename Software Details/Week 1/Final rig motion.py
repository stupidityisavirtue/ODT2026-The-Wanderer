from machine import Pin, I2C
import ssd1306
import time

# ─── OLED ───────────────────────────
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# ─── BUTTONS ────────────────────────
btn_up    = Pin(12, Pin.IN, Pin.PULL_UP)
btn_left  = Pin(14, Pin.IN, Pin.PULL_UP)
btn_down  = Pin(27, Pin.IN, Pin.PULL_UP)
btn_right = Pin(32, Pin.IN, Pin.PULL_UP)

# ─── CENTER + SIZE ──────────────────
cx = 64
cy = 32
offset = 6
move = 6

def read_buttons():
    return {
        "UP":    not btn_up.value(),
        "LEFT":  not btn_left.value(),
        "DOWN":  not btn_down.value(),
        "RIGHT": not btn_right.value()
    }

while True:
    buttons = read_buttons()

    # BASE (reset every frame)
    A = [cx - offset, cy - offset]  # top-left
    B = [cx + offset, cy - offset]  # top-right
    C = [cx - offset, cy + offset]  # bottom-left
    D = [cx + offset, cy + offset]  # bottom-right

    # ─── LEFT (A + D) ───────────────
    if buttons["LEFT"]:
        A[0] -= move
        D[0] -= move

    # ─── RIGHT (B + C) ──────────────
    elif buttons["RIGHT"]:
        B[0] += move
        C[0] += move

    # ─── UP ─────────────────────────
    elif buttons["UP"]:
        A[1] -= move
        B[1] -= move
        C[1] -= move
        D[1] -= move

        # stretch outward
        A[0] -= 2
        B[0] += 2
        C[0] -= 2
        D[0] += 2

    # ─── DOWN ───────────────────────
    elif buttons["DOWN"]:
        A[1] += move
        B[1] += move
        C[1] += move
        D[1] += move

    # ─── DRAW ───────────────────────
    oled.fill(0)

    for p in [A, B, C, D]:
        oled.fill_rect(int(p[0]), int(p[1]), 2, 2, 1)

    oled.show()
    time.sleep(0.03)

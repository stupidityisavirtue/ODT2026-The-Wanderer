import machine
import time
import sh1106
import random


i2c = machine.I2C(0, scl=machine.Pin(21), sda=machine.Pin(25))


oled = sh1106.SH1106_I2C(128, 64, i2c)


up = machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_UP)
down = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)
left = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
right = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)

oled.fill(0)
oled.show()

#line cordinates for the lanes (have to redo test on the big nimmu oled)
def draw_line(x0, y0, x1, y1, col=1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        oled.pixel(x0, y0, col)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

# redrawing arrows they are coming as blocks?
def draw_arrow_direction(x, y, direction):
    if direction == "up":
        draw_line(x, y-4, x-3, y+2)
        draw_line(x, y-4, x+3, y+2)
        draw_line(x-3, y+2, x+3, y+2)

    elif direction == "down":
        draw_line(x, y+4, x-3, y-2)
        draw_line(x, y+4, x+3, y-2)
        draw_line(x-3, y-2, x+3, y-2)

    elif direction == "left":
        draw_line(x-4, y, x+2, y-3)
        draw_line(x-4, y, x+2, y+3)
        draw_line(x+2, y-3, x+2, y+3)

    elif direction == "right":
        draw_line(x+4, y, x-2, y-3)
        draw_line(x+4, y, x-2, y+3)
        draw_line(x-2, y-3, x-2, y+3)


directions = ["right", "left", "up", "down"]

def slide_arrow(direction):
    x_positions = [76, 86, 96, 106]
    x = random.choice(x_positions)

    start_y = random.randint(-15, 0)

    for y in range(start_y, 64, 4):
        oled.fill(0)

        
        draw_line(64, 50, 128, 50)
        draw_line(64, 0, 64, 64)

        draw_arrow_direction(x, y, direction)

        oled.show()
        time.sleep(0.05)


while True:
    slide_arrow(random.choice(directions))
    #Too Fast gotta debug the speed

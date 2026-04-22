#	working

import machine #og
import time #og
import random #og
import framebuf #og
import sh1106 #og
import ssd1306 # Importing the driver saved on your microcontroller

# --- Animation Frame Imports ---
# These import your custom bytearray files for the SSD1306
import idle
import up
import down
import left
import right
import error

# --- Configuration ---
SCL_PIN = 18 #og
SDA_PIN = 19 #og

# SSD1306 Pins for the second display
SSD1306_SCL = 22
SSD1306_SDA = 23

# PIN MAPPINGS (Active LOW with internal pull-up)	
right_button = 12 #og
down_button   = 14 #og
up_button     = 32 #og
left_button   = 27 #og

LANE_WIDTH = 24 #og
HIT_LINE_Y = 43 #og
GOOD_WINDOW = 250 #og

# --- Initialization ---

# Initialize I2C 0 for the SH1106 Game Display
i2c0 = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN), freq=400000) #og
display = sh1106.SH1106_I2C(128, 64, i2c0) #og

# Initialize I2C 1 for the SSD1306 Animation Display
i2c1 = machine.I2C(1, scl=machine.Pin(SSD1306_SCL), sda=machine.Pin(SSD1306_SDA), freq=400000)
anim_display = ssd1306.SSD1306_I2C(128, 64, i2c1)

# Buffer to handle the conversion between your HLSB bitmaps and SSD1306 VLSB format
anim_buffer = bytearray(128 * 8)
anim_fb = framebuf.FrameBuffer(anim_buffer, 128, 64, framebuf.MONO_VLSB)

def update_ssd1306_animation(state):
    """Selects the correct bytearray and updates the SSD1306 display."""
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
    
    # Blit the HLSB data into the VLSB buffer
    temp_fb = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    anim_fb.fill(0)
    anim_fb.blit(temp_fb, 0, 0)
    anim_display.buffer = anim_buffer
    anim_display.show()

# Initialize button pins with internal PULL_UP
pins = [
    machine.Pin(right_button, machine.Pin.IN, machine.Pin.PULL_UP), #og
    machine.Pin(down_button,   machine.Pin.IN, machine.Pin.PULL_UP), #og
    machine.Pin(up_button,     machine.Pin.IN, machine.Pin.PULL_UP), #og
    machine.Pin(left_button,   machine.Pin.IN, machine.Pin.PULL_UP)  #og
]

# --- Arrow Bitmaps for SH1106 ---
arrow_left = bytearray([0x18,0x3C,0x7E,0x18,0x18,0x18,0x00,0x00]) #og
arrow_right = bytearray([0x18,0x18,0x18,0x7E,0x3C,0x18,0x00,0x00]) #og
arrow_up = bytearray([0x10,0x18,0x1C,0xFE,0x1C,0x18,0x10,0x00]) #og
arrow_down = bytearray([0x08,0x18,0x38,0xFE,0x38,0x18,0x08,0x00]) #og

def draw_arrow_direction(x, y, direction):
    """Draws the small arrows on the SH1106 game lanes."""
    if direction == "up": #og
        fb = framebuf.FrameBuffer(arrow_up, 8, 8, framebuf.MONO_VLSB) #og
    elif direction == "down": #og
        fb = framebuf.FrameBuffer(arrow_down, 8, 8, framebuf.MONO_VLSB) #og
    elif direction == "left": #og
        fb = framebuf.FrameBuffer(arrow_left, 8, 8, framebuf.MONO_VLSB) #og
    else: #og
        fb = framebuf.FrameBuffer(arrow_right, 8, 8, framebuf.MONO_VLSB) #og
    display.blit(fb, x-4, y-4) #og

# --- Game State ---
combo = 0 #og
errors = 0 #og
last_hit_time = 0 #og
animation_frame = 0 #og
pet_state = "idle" #og
last_btn_states = [False, False, False, False] #og

# --- Note Generation ---
notes = [] #og
current_note_time = 2000 #og
for i in range(50): #og
    current_note_time += 2000 #og
    notes.append({ #og
        "time": current_note_time, #og
        "lane": random.randint(0, 3), #og
        "hit": False, #og
        "passed": False #og
    }) #og

# --- Main Game Loop ---
def main():
    global combo, errors, pet_state, animation_frame, last_hit_time, last_btn_states

    start_time = time.ticks_ms() #og
    current_anim_state = "idle"
    update_ssd1306_animation("idle") # Initial pet state

    while True:
        display.fill(0) #og
        current_time = time.ticks_diff(time.ticks_ms(), start_time) #og

        # Draw Lanes on SH1106
        for i in range(5): #og
            display.vline(i * LANE_WIDTH, 0, 64, 1) #og
        display.hline(0, HIT_LINE_Y, LANE_WIDTH * 4, 1) #og

        # --- Input Detection (Edge Detection) ---
        current_btn_states = [not p.value() for p in pins] #og
        btn_pressed = [False, False, False, False] #og
        for i in range(4): #og
            if current_btn_states[i] and not last_btn_states[i]: #og
                btn_pressed[i] = True #og
        last_btn_states = current_btn_states #og

        # --- Process Notes and Hit Detection ---
        for note in notes: #og
            if not note["hit"] and not note["passed"]: #og
                dist = note["time"] - current_time #og
                y = int(HIT_LINE_Y - (dist / 30)) #og
                lane = note["lane"] #og
                direction = ["right", "down", "up", "left"][lane] #og

                if -10 < y < 64: #og
                    lane_x = lane * LANE_WIDTH + (LANE_WIDTH // 2) #og
                    draw_arrow_direction(lane_x, y, direction) #og

                # Hit Detection Logic
                if abs(dist) < GOOD_WINDOW: #og
                    if btn_pressed[lane]: #og
                        print("NICE - {} HIT".format(direction.upper())) #og
                        note["hit"] = True #og
                        combo += 1 #og
                        pet_state = direction # Trigger direction animation
                        last_hit_time = current_time #og
                        btn_pressed[lane] = False #og
                
                # Miss Detection Logic
                elif dist < -GOOD_WINDOW: #og
                    note["passed"] = True #og
                    errors += 1 #og
                    print("ERROR: {} MISSED".format(direction.upper())) #og
                    pet_state = "error" # Trigger error animation
                    last_hit_time = current_time #og

        # --- Wrong Button Detection ---
        if any(btn_pressed): #og
            for i in range(4): #og
                if btn_pressed[i]: #og
                    print("WRONG BUTTON PRESSED: Lane {}".format(i)) #og
            pet_state = "error" # Trigger error animation
            last_hit_time = current_time #og

        # Reset pet to idle after 500ms
        if time.ticks_diff(current_time, last_hit_time) > 500: #og
            pet_state = "idle" #og

        # --- SSD1306 Animation Update ---
        # Only update the second OLED if the state has changed to keep game smooth
        if pet_state != current_anim_state:
            update_ssd1306_animation(pet_state)
            current_anim_state = pet_state

        # --- UI Text on SH1106 ---
        display.text("E:{}".format(errors), 98, 30, 1) #og
        display.text("C:{}".format(combo), 98, 50, 1) #og

        display.show() #og
        time.sleep_ms(5) #og

if __name__ == "__main__":
    main() #og

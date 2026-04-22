import machine
import time
import sh1106
import random


# I2C Pins
SCL_PIN = 21
SDA_PIN = 25

# Button Pins 
BTN_RIGHT1 = 12
BTN_DOWN   = 14
BTN_UP     = 32
BTN_RIGHT2 = 34 # Input only

# Game Constants
LANE_WIDTH = 24 # Adjusted for animation space check it out arshia
HIT_LINE_Y = 56
NOTE_SPEED = 2  # 
PERFECT_WINDOW = 50 # ms
GOOD_WINDOW = 100    # ms format basically all os these are those


i2c = machine.I2C(0, scl=machine.Pin(SCL_PIN), sda=machine.Pin(SDA_PIN), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c)

# Buttons

pins = [
    machine.Pin(BTN_RIGHT1, machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(BTN_DOWN,   machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(BTN_UP,     machine.Pin.IN, machine.Pin.PULL_UP),
    machine.Pin(BTN_RIGHT2, machine.Pin.IN) 
]


# These are now initialized globally and will be declared global in main()
score = 0
combo = 0
last_hit_time = 0
animation_frame = 0
pet_state = "idle" # idle, happy, sad

# Note Chart: (time_ms, lane)
# Lanes: 0=Right1, 1=Down, 2=Up, 3=Right2
notes = []
for i in range(50):
    notes.append({"time": 2000 + i * 800, "lane": random.randint(0, 3), "hit": False, "passed": False})

def draw_pet(x, y, state, frame):
    """Draws a cute little blob pet that reacts to keys."""
    # Body
    display.fill_rect(x, y, 20, 20, 0) # Clear area
    display.rect(x, y, 20, 20, 1)      # Outline
    
    # Eyes
    eye_y = y + 5 + (1 if frame % 10 > 5 else 0) # Blink/bounce
    if state == "idle":
        display.pixel(x + 6, eye_y, 1)
        display.pixel(x + 14, eye_y, 1)
        display.hline(x + 8, y + 14, 4, 1) # Neutral mouth
    elif state == "happy":
        display.line(x + 5, eye_y, x + 7, eye_y - 2, 1) # ^ ^ eyes
        display.line(x + 7, eye_y - 2, x + 9, eye_y, 1)
        display.line(x + 11, eye_y, x + 13, eye_y - 2, 1)
        display.line(x + 13, eye_y - 2, x + 15, eye_y, 1)
        display.rect(x + 8, y + 12, 4, 4, 1) # Big mouth
    elif state == "sad":
        display.line(x + 6, eye_y, x + 8, eye_y + 2, 1) # x x eyes
        display.line(x + 8, eye_y, x + 6, eye_y + 2, 1)
        display.line(x + 14, eye_y, x + 12, eye_y + 2, 1)
        display.line(x + 12, eye_y, x + 14, eye_y + 2, 1)
        display.hline(x + 8, y + 15, 4, 1) # Flat mouth

def main():
    global score, combo, pet_state, animation_frame, last_hit_time
    
    start_time = time.ticks_ms()
    
    print("Game Started!")
    
    while True:
        display.fill(0)
        current_time = time.ticks_diff(time.ticks_ms(), start_time)
        
        # 1. Draw Lanes & Hit Line
        for i in range(5):
            display.vline(i * LANE_WIDTH, 0, 64, 1)
        display.hline(0, HIT_LINE_Y, LANE_WIDTH * 4, 1)
        
        # 2. Handle Input
        btn_states = [not p.value() for p in pins]
        
        # 3. Update & Draw Notes
        for note in notes:
            if not note["hit"] and not note["passed"]:
                # Calculate Y position
                # Note should be at HIT_LINE_Y when current_time == note["time"]
                dist_from_hit = note["time"] - current_time
                note_y = HIT_LINE_Y - int(dist_from_hit / 10) # 10ms per pixel
                
                if note_y > -10 and note_y < 64:
                    display.fill_rect(note["lane"] * LANE_WIDTH + 4, note_y, LANE_WIDTH - 8, 4, 1)
                
                # Check for Hit
                if btn_states[note["lane"]] and abs(dist_from_hit) < GOOD_WINDOW:
                    note["hit"] = True
                    combo += 1
                    score += 100 if abs(dist_from_hit) < PERFECT_WINDOW else 50
                    pet_state = "happy"
                    last_hit_time = current_time
                
                # Check for Miss
                if dist_from_hit < -GOOD_WINDOW:
                    note["passed"] = True
                    combo = 0
                    pet_state = "sad"
                    last_hit_time = current_time

        # 4. Pet Animation Logic
        if time.ticks_diff(current_time, last_hit_time) > 500:
            pet_state = "idle"
        
        animation_frame += 1
        draw_pet(102, 20, pet_state, animation_frame)
        
        # 5. UI
        display.text("S:{}".format(score), 98, 0, 1)
        display.text("C:{}".format(combo), 98, 50, 1)
        
        display.show()
        
        # Small delay to control frame rate
        time.sleep_ms(10)

if __name__ == "__main__":
    main()
    
    #Work Work Base code with some weird ass expression code 
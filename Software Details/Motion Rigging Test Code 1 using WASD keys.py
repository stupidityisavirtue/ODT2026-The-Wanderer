# Wokwi Simulation Code :( I CANT DO THIS 8TH code
import machine
import ssd1306
import time
import sys

#PINS BRRR intialization
I2C_SCL = 22
I2C_SDA = 21
WIDTH = 128
HEIGHT = 64

# Oled Oled Oled Oled BRRRRRR

try:
    i2c = machine.I2C(0, scl=machine.Pin(I2C_SCL), sda=machine.Pin(I2C_SDA))
    oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
except Exception as e:
    print("OLED initialization failed:", e)
    
    class MockOLED:
        def __init__(self): pass
        def fill(self, c): pass
        def pixel(self, x, y, c): pass
        def show(self): pass
        def text(self, t, x, y): print(f"OLED: {t} at {x},{y}")
    oled = MockOLED()

# wwiwiwiwi
CHARACTER_BASE = [
    "      ########      ",
    "    ############    ",
    "   ##############   ",
    "  ################  ",
    " ################## ",
    " ################## ",
    " ################## ",
    " ################## ",
    "  ################  ",
    "   ##############   ",
    "    ############    ",
    "      ########      ",
    "       ######       ",
    "        ####        ",
    "         ##         ",
    "        ####        ",
    "       ######       ",
    "      ########      ",
    "     ##########     ",
    "    ############    ",
    "   ##############   ",
    "  ################  ",
    " ################## ",
    " ################## ",
]

def draw_character(x_offset, y_offset, hand_pos=0, leg_pos=0):
    """
    hand_pos: 0=middle, 1=up, -1=down
    leg_pos: 0=middle, 1=up, -1=down
    """
    oled.fill(0)
    
    # Mathematic STRUCTURE (5th test)
    cx = x_offset + 22
    cy = y_offset + 10
    
    # Simple head shape
    for r, row in enumerate(CHARACTER_BASE[:14]):
        for c, pixel in enumerate(row):
            if pixel == '#':
                oled.pixel(cx + c, cy + r, 1)
                
    # Draw Body 1.3
    for r, row in enumerate(CHARACTER_BASE[14:20]):
        for c, pixel in enumerate(row):
            if pixel == '#':
                oled.pixel(cx + c, cy + r + 14, 1)
                
    # Draw Hands (Dynamic) 1.1
    # Left Hand move
    hx_l = cx - 2
    hy_l = cy + 16
    if hand_pos == 1: # Up move
        oled.pixel(hx_l, hy_l - 4, 1)
        oled.pixel(hx_l - 1, hy_l - 5, 1)
    elif hand_pos == -1: # Down move
        oled.pixel(hx_l, hy_l + 4, 1)
        oled.pixel(hx_l - 1, hy_l + 5, 1)
    else: # Middle movemove
        oled.pixel(hx_l - 2, hy_l, 1)
        oled.pixel(hx_l - 3, hy_l, 1)
        
    # Right Hand
    hx_r = cx + 22
    hy_r = cy + 16
    if hand_pos == 1: # Up
        oled.pixel(hx_r, hy_r - 4, 1)
        oled.pixel(hx_r + 1, hy_r - 5, 1)
    elif hand_pos == -1: # Down
        oled.pixel(hx_r, hy_r + 4, 1)
        oled.pixel(hx_r + 1, hy_r + 5, 1)
    else: # Middle
        oled.pixel(hx_r + 2, hy_r, 1)
        oled.pixel(hx_r + 3, hy_r, 1)

    # Draw Legs (Dynamic)
    lx_l = cx + 5
    lx_r = cx + 15
    ly = cy + 24
    if leg_pos == 1: # Up (bent)
        oled.pixel(lx_l, ly - 2, 1)
        oled.pixel(lx_r, ly - 2, 1)
    elif leg_pos == -1: # Down (extended)
        oled.pixel(lx_l, ly + 4, 1)
        oled.pixel(lx_r, ly + 4, 1)
    else: # Middle
        oled.pixel(lx_l, ly + 2, 1)
        oled.pixel(lx_r, ly + 2, 1)

    oled.show()

def main():
    print("Dancing Character Started!")
    print("Use Arrow Keys (or WASD) to dance!")
    
    hand = 0
    leg = 0
    
   
    draw_character(0, 0, hand, leg)
    
    
    import uselect
    spoll = uselect.poll()
    spoll.register(sys.stdin, uselect.POLLIN)
    
    while True:
        if spoll.poll(100): # Check for input every 100ms
            char = sys.stdin.read(1)
            
            # Handle Arrow Keys 
            if char == '\x1b': 
                next1 = sys.stdin.read(1)
                if next1 == '[':
                    direction = sys.stdin.read(1)
                    if direction == 'A': 
                        hand = 1
                        leg = 1
                    elif direction == 'B': 
                        hand = -1
                        leg = -1
                    elif direction == 'C': 
                        hand = 1
                        leg = -1
                    elif direction == 'D': 
                        hand = -1
                        leg = 1
            
            
                hand, leg = 1, 1
            elif char.lower() == 's':
                hand, leg = -1, -1
            elif char.lower() == 'd':
                hand, leg = 1, -1
            elif char.lower() == 'a':
                hand, leg = -1, 1
            
            # Update display
            draw_character(0, 0, hand, leg)
            time.sleep(0.1)
            
            # Reset to neutral after a short delay to make it look like a "move"
            draw_character(0, 0, 0, 0)
            hand, leg = 0, 0

if __name__ == "__main__":
    main()

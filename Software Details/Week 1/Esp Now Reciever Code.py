import network
import espnow

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

e = espnow.ESPNow()
e.active(True)

system_on = False

print("Waiting for start...")

while True:
    host, msg = e.recv() #host giving hahahha ew'

    if msg:#no debugging and checks only when input exists
        
        vals = msg.decode().split(',')#so understands and breaks aka splits it into a list cuz we have a list in console code the up down bs

        up, down, left, right, jump, start, stop = vals

        if start == '0' and not system_on: #system IS NOT ON WITHOUT START which is why we are starting with false
            system_on = True
            print("System Started")

        if stop == '0' and system_on:
            system_on = False
            print("Stopping System")
            continue

        if not system_on:
            continue #just like pass function 

        if up == '0':
            print("UP clicked")
        if down == '0':
            print("DOWN clicked")
        if left == '0':
            print("LEFT clicked")
        if right == '0':
            print("RIGHT clicked")
        if jump == '0':
            print("JUMP clicked")
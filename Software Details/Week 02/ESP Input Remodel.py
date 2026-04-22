#Call the esp 32 like TELL IT then import your pins cuz the machine has to know
from machine import Pin
#I have to import time cuz IT NEEDS to know that Im having a time factor
import time
#I made and defined their lives so I basically told them WHERE their house is, it has to be defined to know what pin it is from and if it is input or not
button1 = (4,Pin.IN,Pin.PULL_UP)
button2 = (16,Pin.IN,Pin.PULL_UP)
#I need it to read this statement continously it shouldn't be a one time thing
while True:
# we dont need else statement cuz if input isnt there how will it work?
    button1_val = button1.value()
    button2_val = button2.value()
    elif button1_val == 0:
            print("Only button 1 pressed")
            time.sleep(0.2)
        # = here means Im assigning value and == and means Im checking if this condition can occur
    elif button2_val == 0:
            print("Only button 2 pressed")
            time.sleep(0.2)
        #This is to show both buttons press, elif considers only one statement
    if button1.value() == 0 and button2.value() == 0 :
        print("Both Buttons Pressed")
        
    


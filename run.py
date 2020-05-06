import time, random

from modules.SreenReader import *
from modules.Control import *
import modules.Neyro

control = СontrolClass(1)

ScreenReader = ScreenReaderClass((165, 30, 1201, 738))

press_power = 0

while True:
    x, _ =  ScreenReader.GetRoadMoment()
    if(abs(x - ((1201-165)/2)) < 200):
        if(press_power >= 6):
            control.SetButton(2, 1)
        else:
            control.SetButton(2, 0)
        press_power += 1
        if(press_power == 11): press_power = 0
        control.SetButton(1, 0)
        
    else:
        control.SetButton(2, 0)
        #control.SetButton(1, 1)

    if(x > ((1201-165)/2) and abs(x - ((1201-165)/2)) > 10):
        control.SetLeftStick(1, -1)
    elif(x < ((1201-165)/2) and abs(x - ((1201-165)/2)) > 10):
        control.SetLeftStick(-1, -1)
    else:
        control.SetLeftStick(0, 0)
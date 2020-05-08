import time, random

from modules.SreenReader import *
from modules.Control import *

control = СontrolClass(1)
time.sleep(5)

ScreenReader = ScreenReaderClass((165, 30, 1201, 738))

press_power = 0

ScreenReader.StartDemon()

while True:

    (x1, _), (x2, _) =  ScreenReader.GetRoadMoment()
    if(abs(x1 - ((1201-165)/2)) < 110):
        if(press_power >= 0):  control.SetButton(2, 1) # газ
        else: control.SetButton(2, 0)
        press_power += 1
        if(press_power == 11): press_power = 0 # газ работает 4 из 10

        control.SetButton(1, 0) 
    elif(abs(x1 - ((1201-165)/2)) < 150):
        control.SetButton(2, 0)
    else:
        control.SetButton(1, 0) 


    if(x1 > ((1201-165)/2) and abs(x1 - ((1201-165)/2)) > 60):
        control.SetLeftStick(1, -1) 
    elif(x1 < ((1201-165)/2) and abs(x1 - ((1201-165)/2)) > 60):
        control.SetLeftStick(-1, -1) 
    else:
        control.SetLeftStick(0, 0)

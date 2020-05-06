from modules.Control import *
import time
control = СontrolClass()

time.sleep(5)

# for Fusion 3.64
SetStick = [(0, 1), (0, -1), (-1, 0), (1, 0)]
SetButton = [1, 2, 3, -1, 4, 5, 6, 11]

for i in SetStick:
    print("stick")
    control.SetLeftStick(i[0], i[1])
    time.sleep(0.5)
    control.SetLeftStick(0, 0)
    time.sleep(1)

for i in SetButton:
    if(i==-1):
        print("PRESS START")
        time.sleep(3)
        continue
    print("button")
    control.SetButton(i, 1)
    time.sleep(0.15)
    control.SetButton(i, 0)
    time.sleep(1)

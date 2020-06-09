import time, random

from modules.SreenReader import *
from modules.Control import *
from modules.ML import *

control = СontrolClass(1)

NumberOfPersons = 15
TestingTime = 1

time.sleep(5)

ScreenReader = ScreenReaderClass((64, 32, 576, 448))
Genetic = GeneticAlgorithm(NumberOfPersons, (21, 32, 4))
ScreenReader.StartDemon()
ScreenReader.GetSpeed(None, True)

ERA = 5
k = 0.15

ScreenReader.SetStatistics(Genetic.GetStatistics())

while True:
    for i in range(NumberOfPersons):

        control.PressKeyOnKeyboard('f8')
        TimeStart = time.time()
        count = 0

        while True:
            x =  ScreenReader.GetRoadMoment(10)
            y = ScreenReader.GetRoadMoment(10, Mask=ScreenReader.RED_MASK_CAR, Save=True)
            for j in y: x.append(j)
            Speed = ScreenReader.GetSpeed()
            x.append(Speed/200)

            result = Genetic.Persons[i].Predict(x)

            if(result[0] > 0): control.SetButton(2, 1)
            else: control.SetButton(2, 0)

            if(result[1] > 0): control.SetButton(1, 1)
            else: control.SetButton(1, 0)

            if(result[2] > 0 and result[3] > 0): control.SetLeftStick(0, 0)
            elif(result[2] > 0): control.SetLeftStick(1, 0)
            elif(result[3] > 0): control.SetLeftStick(-1, 0)

            devigation = abs((abs(x[0])-0.5)*2)
            
            Genetic.Persons[i].Performance += (ScreenReader.GetSpeed()/200)
            #if(Genetic.Persons[i].Performance < 0): Genetic.Persons[i].Performance = 0
            Genetic.Persons[i].Speed += ScreenReader.GetSpeed()
            #if(Genetic.Persons[i].Speed < 0): Genetic.Persons[i].Speed = 0

            #if((time.time() - TimeStart) > 5 and Genetic.Persons[i].Speed < 25): break
            if((time.time() - TimeStart) > TestingTime): break

            count += 1
        Genetic.Persons[i].Speed /= count
        ScreenReader.SetStatistics(Genetic.GetStatistics())
   
    ERA+=1

    Genetic.NewEra()
    time.sleep(3)
    
    for i in range(NumberOfPersons): Genetic.Persons[i].Reset()
    ScreenReader.SetStatistics(Genetic.GetStatistics())


    TestingTime += ERA

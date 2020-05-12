import time, random

from modules.SreenReader import *
from modules.Control import *
from modules.ML import *

control = СontrolClass(1)

NumberOfPersons = 10
TestingTime = 5

time.sleep(5)

ScreenReader = ScreenReaderClass((64, 32, 576, 448))
Genetic = GeneticAlgorithm(NumberOfPersons, (21, 9, 3))
ScreenReader.StartDemon()
ScreenReader.GetSpeed(None, True)

ERA = 1
k = 0.15

ScreenReader.SetStatistics(Genetic.GetStatistics())

while True:
    for i in range(NumberOfPersons):

        control.PressKeyOnKeyboard('f8')
        TimeStart = time.time()

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

            control.SetLeftStick(round(result[2]), 0)

            Genetic.Persons[i].Performance += (ScreenReader.GetSpeed()/200 - abs(x[len(x)-2]))
            #if(Genetic.Persons[i].Performance < 0): Genetic.Persons[i].Performance = 0
            Genetic.Persons[i].Speed = k*ScreenReader.GetSpeed() + Genetic.Persons[i].Speed*(1-k)
            #if(Genetic.Persons[i].Speed < 0): Genetic.Persons[i].Speed = 0

            if((time.time() - TimeStart) > TestingTime): break

        ScreenReader.SetStatistics(Genetic.GetStatistics())
   
    ERA+=1

    Performances = []
    for i in range(NumberOfPersons): Performances.append(Genetic.Persons[i].Performance)
    for i in range(NumberOfPersons): Genetic.Persons[i].Performance += min(Performances)+1


    Genetic.NewEra()
    time.sleep(3)
    
    for i in range(NumberOfPersons):
        Genetic.Persons[i].Performance = -1
        Genetic.Persons[i].Speed = -1
    ScreenReader.SetStatistics(Genetic.GetStatistics())


    TestingTime += ERA

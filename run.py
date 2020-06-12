import time, random

from modules.SreenReader import *
from modules.Control import *
from modules.ML import *

control = СontrolClass(1)

NumberOfPersons = 15
TestingTime = 5

time.sleep(5)

ScreenReader = ScreenReaderClass((64, 32, 576, 448))
Genetic = GeneticAlgorithm(NumberOfPersons, (41, 64, 3))
ScreenReader.StartDemon()
ScreenReader.GetSpeed(None, True)

ERA = 1
k = 0.15

ScreenReader.SetStatistics(Genetic.GetStatistics())

while True:
    for i in range(NumberOfPersons):

        control.PressKeyOnKeyboard('f8')
        TimeStart = time.time()
        count = 0

        while True:
            x1, x2 = ScreenReader.GetRoadMoment(10)
            y1, y2 = ScreenReader.GetRoadMoment(10, Mask=ScreenReader.RED_MASK_CAR)
            Speed = ScreenReader.GetSpeed()
            NeyroInput = x1+x2+y1+y2
            NeyroInput.append(Speed/200)
            result = Genetic.Persons[i].Predict(NeyroInput)

            if(result[0] > 0): control.SetButton(2, 1)
            else: control.SetButton(2, 0)

            if(result[1] > 0): control.SetButton(1, 1)
            else: control.SetButton(1, 0)

            control.SetLeftStick(result[2], 0)

            devigation = abs((abs(x1[0])-0.5)*2)
            
            Genetic.Persons[i].Performance += (ScreenReader.GetSpeed()/200)
            #if(Genetic.Persons[i].Performance < 0): Genetic.Persons[i].Performance = 0
            Genetic.Persons[i].Speed += ScreenReader.GetSpeed()
            #if(Genetic.Persons[i].Speed < 0): Genetic.Persons[i].Speed = 0

            #if((time.time() - TimeStart) > 5 and Genetic.Persons[i].Speed < 25): break
            if((time.time() - TimeStart) > TestingTime): break

            count += 1

        #print(Genetic.Persons[i].MemoryHiddenNeurons[random.randint(0, 10)])
        #print(Genetic.Persons[i].WeightsMemoryHiddenNeurons[random.randint(0, 10)])

        Genetic.Persons[i].Speed = int(Genetic.Persons[i].Speed/count)
        Genetic.Persons[i].Performance = int(Genetic.Persons[i].Performance/TestingTime*10)
        
        ScreenReader.SetStatistics(Genetic.GetStatistics())
        
        print(count/TestingTime)
    ERA+=1

    Genetic.NewEra()
    time.sleep(3)
    
    for i in range(NumberOfPersons): Genetic.Persons[i].Reset()
    ScreenReader.SetStatistics(Genetic.GetStatistics())

    TestingTime += 1#ERA

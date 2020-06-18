import time, random

from modules.SreenReader import *
from modules.Control import *
from modules.ML import *

control = ControlClass(1)

NumberOfPersons = 15
TestingTime = 5

SizeInputImage = (64, 16)

time.sleep(1)

ScreenReader = ScreenReaderClass((64, 32, 576, 448))
#Genetic = GeneticAlgorithm(NumberOfPersons, (41 + (SizeInputImage[0]*SizeInputImage[1]*3), 80, 3))
Genetic = GeneticAlgorithm(NumberOfPersons, (1+(SizeInputImage[0]*SizeInputImage[1]*3), 1024, 3))
ScreenReader.StartDemon()
ScreenReader.GetSpeed(None, True)

ScreenReader.SreenShotMini(ScreenReader.ScreenShotingAreaRoad, SizeInputImage, Save=True)

ERA = 1
k = 0.15

ScreenReader.SetStatistics(Genetic.GetStatistics())


#print("----------------- LOAD -----------------")
#for i in range(NumberOfPersons): 
#    Genetic.Persons[i].Load("./NeyroData/Person{}.txt".format(i+1))
#    print("Load person", i+1)

while True:
    for i in range(NumberOfPersons):

        control.PressKeyOnKeyboard('f8')
        TimeStart = time.time()
        count = 0

        while True:
            #x1, x2 = ScreenReader.GetRoadMoment(10)
            #y1, y2 = ScreenReader.GetRoadMoment(10, Mask=ScreenReader.RED_MASK_CAR)
            Speed = ScreenReader.GetSpeed()

            #NeyroInput = np.array(x1+x2+y1+y2)
            #NeyroInput = np.append(NeyroInput, Speed/200)

            MiniImage = np.array(ScreenReader.SreenShotMini(ScreenReader.ScreenShotingAreaRoad, SizeInputImage))
            MiniImageReshape = np.reshape(MiniImage, SizeInputImage[0]*SizeInputImage[1]*3)
            MiniImageReshape =  MiniImageReshape / 255
            #result = Genetic.Persons[i].Predict(np.append(NeyroInput, MiniImageReshape))
            result = Genetic.Persons[i].Predict(np.append(Speed/200, MiniImageReshape))

            if(result[0] > 0): control.SetButton(2, 1)
            else: control.SetButton(2, 0)

            if(result[1] > 0): control.SetButton(1, 1)
            else: control.SetButton(1, 0)

            control.SetLeftStick(result[2], 0)

            #devigation = abs((abs(x1[0])-0.5)*2)
            
            Genetic.Persons[i].Performance += (ScreenReader.GetSpeed()/200)
            Genetic.Persons[i].Speed += ScreenReader.GetSpeed()

            #if((time.time() - TimeStart) > 5 and Genetic.Persons[i].Speed < 25): break
            if((time.time() - TimeStart) > TestingTime): break

            count += 1

        #print(Genetic.Persons[i].MemoryHiddenNeurons[random.randint(0, 10)])
        #print(Genetic.Persons[i].WeightsMemoryHiddenNeurons[random.randint(0, 10)])

        Genetic.Persons[i].Speed = int(Genetic.Persons[i].Speed/count)
        Genetic.Persons[i].Performance = int(Genetic.Persons[i].Performance/TestingTime*10)
        
        ScreenReader.SetStatistics(Genetic.GetStatistics())
        
        print(count/TestingTime)
        
    if(ERA%5 == 0):
        print("----------------- SAVE -----------------")
        for i in range(NumberOfPersons): 
            Genetic.Persons[i].Save("./NeyroData/Person{}.txt".format(i+1))
            print("Save person", i+1)

    ERA+=1
    Genetic.NewEra()
    
    for i in range(NumberOfPersons): Genetic.Persons[i].Reset()
    ScreenReader.SetStatistics(Genetic.GetStatistics())

    TestingTime += 1#ERA
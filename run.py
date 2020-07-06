import time, random

from modules.SreenReader import *
from modules.Control import *
from modules.ML import *

control = ControlClass(1)

NumberOfPersons = 15
TestingTime = 30

SizeInputImage = (64, 16)

time.sleep(1)

ScreenReader = ScreenReaderClass((64, 32, 576, 448))
Genetic = GeneticAlgorithm(NumberOfPersons, (1+(SizeInputImage[0]*SizeInputImage[1]*3), 1024, 3))
ScreenReader.StartDemon()
ScreenReader.GetSpeed(None, True)

ERA = 1
k = 0.15
control.SetButton(2, 1)
ScreenReader.SetStatistics(Genetic.GetStatistics())

print("----------------- LOAD -----------------")
for i in range(NumberOfPersons): 
    Genetic.Persons[i].Load("./NeyroData/Person{}.txt".format(i+1))
    print("Load person", i+1)
    
ScreenReader.SreenShotMini(ScreenReader.ScreenShotingAreaRoad, SizeInputImage, Save=True)

while True:
    for i in range(NumberOfPersons):

        control.PressKeyOnKeyboard('f8')
        TimeStart = time.time()
        count = 0

        while True:
            Speed = ScreenReader.GetSpeed()

            MiniImage = np.array(ScreenReader.SreenShotMini(ScreenReader.ScreenShotingAreaRoad, SizeInputImage))
            MiniImageReshape = np.reshape(MiniImage, SizeInputImage[0]*SizeInputImage[1]*3)
            MiniImageReshape =  MiniImageReshape / 255
            result = Genetic.Persons[i].Predict(np.append(Speed/200, MiniImageReshape))

            if(result[0] > 0): control.SetButton(2, 1)
            else: control.SetButton(2, 0)

            if(result[1] > 0): control.SetButton(1, 1)
            else: control.SetButton(1, 0)

            control.SetLeftStick(result[2], 0)

            
            Genetic.Persons[i].Performance += (ScreenReader.GetSpeed()/200)
            Genetic.Persons[i].Speed += ScreenReader.GetSpeed()

            #if((time.time() - TimeStart) > 5 and Genetic.Persons[i].Speed < 25): break
            if((time.time() - TimeStart) > TestingTime): break

            count += 1

        Genetic.Persons[i].Speed = int(Genetic.Persons[i].Speed/count)
        Genetic.Persons[i].Performance = int(Genetic.Persons[i].Performance/TestingTime*10)
        
        ScreenReader.SetStatistics(Genetic.GetStatistics())
        
        print(count/TestingTime)
        
    if(ERA%5 == 0):
        print("----------------- SAVE -----------------")
        for i in range(NumberOfPersons): 
            Genetic.Persons[i].Save("./NeyroData/Person{}.txt".format(i+1))
            print("Save person", i+1)

    minScore = 10000
    maxScore = -10000
    minSpeed = 200
    maxSpeed = -1
    for i in range(NumberOfPersons):
        if(Genetic.Persons[i].Performance > maxScore): maxScore = Genetic.Persons[i].Performance
        if(Genetic.Persons[i].Performance < minScore): minScore = Genetic.Persons[i].Performance
        if(Genetic.Persons[i].Speed > maxSpeed): maxSpeed = Genetic.Persons[i].Speed
        if(Genetic.Persons[i].Speed < minSpeed): minSpeed = Genetic.Persons[i].Speed

    LogFile = open("Progress.txt", "a")
    writeString = time.strftime("%d.%m.%Y %X", time.gmtime(time.time())) + f" {minScore}, {maxScore}; {minSpeed}, {maxSpeed}\n"
    print("----------------- WRITE PROGRESS FILE -----------------")
    print(writeString)
    LogFile.write(writeString)
    LogFile.close()

    ERA+=1
    Genetic.NewEra()
    
    for i in range(NumberOfPersons): Genetic.Persons[i].Reset()
    ScreenReader.SetStatistics(Genetic.GetStatistics())

    TestingTime += 1#ERA
    if(TestingTime > 60): TestingTime = 60
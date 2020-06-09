import random, math
import numpy as np

class Neyro():
    def __init__(self, NumberInputs, NumberHiddenNeyrons, NumberOutputs):
        self.Performance = -1
        self.Speed = -1
        self.Deviation = 0

        self.NumberInputs = NumberInputs + 1 # +1 for bias node
        self.NumberHiddenNeyrons = NumberHiddenNeyrons
        self.NumberOutputs = NumberOutputs

        self.ValuesInputNeurons = np.ones((self.NumberInputs))
        self.ValuesHiddenNeurons = np.ones((self.NumberHiddenNeyrons))
        self.ValuesOutputNeurons = np.ones((self.NumberOutputs))

        self.MemoryHiddenNeurons = np.array([0 for i in range(self.NumberHiddenNeyrons)])
        self.MemoryOutputNeurons = np.array([0 for i in range(self.NumberOutputs)])

        self.WeightsMemoryHiddenNeurons = np.array([0 for i in range(self.NumberHiddenNeyrons)])
        self.WeightsMemoryOutputNeurons = np.array([0 for i in range(self.NumberOutputs)])

        self.InputWeights = np.ones((self.NumberInputs, self.NumberHiddenNeyrons))
        self.OutputWeights = np.ones((self.NumberHiddenNeyrons, self.NumberOutputs))

        for i in range(self.NumberInputs):
            for j in range(self.NumberHiddenNeyrons): self.InputWeights[i, j] = self.Random(-1, 1)
        for j in range(self.NumberHiddenNeyrons):
            for k in range(self.NumberOutputs): self.OutputWeights[j, k] = self.Random(-1, 1)

    def Random(self, a, b):
        return (b-a)*random.random() + a

    def Reset(self):
        self.Performance = -1
        self.Speed = -1
        self.Deviation = 0
        self.MemoryHiddenNeurons = np.array([0 for i in range(self.NumberHiddenNeyrons)])
        self.MemoryOutputNeurons = np.array([0 for i in range(self.NumberOutputs)])

    def makeMatrix(self, width, height, fill=0.0):
        Matrix = []
        for i in range(width):
            Matrix.append([fill]*height)
        return Matrix

    def sigmoid(self, x):
        return math.tanh(x)

    def Predict(self, inputs):
        if len(inputs) != self.NumberInputs-1:
            raise ValueError('Wrong number inputs!')

        for i in range(self.NumberInputs-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ValuesInputNeurons[i] = inputs[i]

        for j in range(self.NumberHiddenNeyrons):
            sum = 0.0
            for i in range(self.NumberInputs):
                sum = sum + self.ValuesInputNeurons[i] * self.InputWeights[i, j]
            self.ValuesHiddenNeurons[j] = \
                self.sigmoid(sum + (self.WeightsMemoryHiddenNeurons[j] * self.MemoryHiddenNeurons[j]))
            self.MemoryHiddenNeurons[j] = self.ValuesHiddenNeurons[j]
        
        for k in range(self.NumberOutputs):
            sum = 0.0
            for j in range(self.NumberHiddenNeyrons):
                sum = sum + self.ValuesHiddenNeurons[j] * self.OutputWeights[j, k]
            self.ValuesOutputNeurons[k] = \
                self.sigmoid(sum + (self.WeightsMemoryOutputNeurons[k] * self.MemoryOutputNeurons[k]))
            self.MemoryOutputNeurons[k] = self.ValuesOutputNeurons[k]

        return self.ValuesOutputNeurons[:]

    def __str__(self): return "Score = "+ str((lambda x: x if(not x==-1) else "unknown")(self.Performance)) +" Speed = "+ \
                                str((lambda x: x if(not x==-1) else "unknown")(self.Speed)) +"\n"



class GeneticAlgorithm():
    def __init__(self, NumberOfPersons=10, Neyrons=(5, 8, 3)):
        self.Persons = [Neyro(Neyrons[0], Neyrons[1], Neyrons[2]) for i in range(NumberOfPersons)]
        self.Neyrons = Neyrons
        self.NumberOfPersons = NumberOfPersons
        self.MutationK = 0.05
        self.Era = 1

    def GeneСalculation(self, Gene1, Gene2, GeneK=0.5, MutationK=0.1, MutationFrom=-1, MutationTo=1):
        if(random.random() < MutationK): return (MutationTo-MutationFrom)*random.random() + MutationFrom;
        else: return (Gene1*GeneK) + (Gene2*(1-GeneK)); 

    def Birth(self, Person1, Person2, GeneK=0.5, MutationK=-1):
        MutationK = (lambda x: self.MutationK if(x==-1) else x)(MutationK)
        OutputPerson = Neyro(self.Neyrons[0], self.Neyrons[1], self.Neyrons[2])

        for i in range(len(Person1.InputWeights)):
            for j in range(len(Person1.InputWeights[0])):
                OutputPerson.InputWeights[i, j] = self.GeneСalculation(Person1.InputWeights[i, j], Person2.InputWeights[i, j], GeneK, MutationK)
        for i in range(len(Person1.OutputWeights)):
            for j in range(len(Person1.OutputWeights[0])):
                OutputPerson.OutputWeights[i, j] = self.GeneСalculation(Person1.OutputWeights[i, j], Person2.OutputWeights[i, j], GeneK, MutationK)

        for i in range(Person1.NumberHiddenNeyrons):
            OutputPerson.WeightsMemoryHiddenNeurons[i] = \
                self.GeneСalculation(Person1.WeightsMemoryHiddenNeurons[i], Person2.WeightsMemoryHiddenNeurons[i], GeneK, MutationK)
        for i in range(Person1.NumberOutputs):
            OutputPerson.WeightsMemoryOutputNeurons[i] = \
                self.GeneСalculation(Person1.WeightsMemoryOutputNeurons[i], Person2.WeightsMemoryOutputNeurons[i], GeneK, MutationK)
        
        return OutputPerson
    
    def NewEra(self):
        self.Era+=1
        self.Sort()
        for i in range(math.ceil(self.NumberOfPersons/2)+1, self.NumberOfPersons, 1):
            RandomPerson1 = round(random.randint(0, math.ceil(self.NumberOfPersons/2)*1000)/1000)
            RandomPerson2 = round(random.randint(0, math.ceil(self.NumberOfPersons/2)*1000)/1000)
            self.Persons[i] = self.Birth(self.Persons[RandomPerson1], self.Persons[RandomPerson2])

    def Sort(self):
        self.Persons = sorted(self.Persons, key=(lambda x: -1*x.Performance))

    def __str__(self):
        Output = "Current ERA - {0} Persons - {1}\n".format(self.Era, len(self.Persons))
        for i in range(len(self.Persons)): Output += "Person {0} ".format(i+1)+ str(self.Persons[i]) +"\n"
        return Output + "\n"

    def GetStatistics(self): return str(self)
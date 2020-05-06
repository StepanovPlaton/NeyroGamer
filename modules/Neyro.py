
class Neyro():
    def __init__(self, NumberInputs, NumberHiddenNeyrons, NumberOutputs):
        self.NumberInputs = NumberInputs + 1 # +1 for bias node
        self.NumberHiddenNeyrons = NumberHiddenNeyrons
        self.NumberOutputs = NumberOutputs

        self.ValuesInputNeurons = [1.0]*self.NumberInputs
        self.ValuesHiddenNeurons = [1.0]*self.NumberHiddenNeyrons
        self.ValuesOutputNeurons = [1.0]*self.NumberOutputs
        
        self.InputWeights = makeMatrix(self.NumberInputs, self.NumberHiddenNeyrons)
        self.OutputWeights = makeMatrix(self.NumberHiddenNeyrons, self.NumberOutputs)

        for i in range(self.NumberInputs):
            for j in range(self.NumberHiddenNeyrons):
                self.InputWeights[i][j] = Random(-1, 1)
        for j in range(self.NumberHiddenNeyrons):
            for k in range(self.NumberOutputs):
                self.OutputWeights[j][k] = Random(-1, 1)

    def Random(a, b):
        return (b-a)*random.random() + a

    def makeMatrix(width, height, fill=0.0):
        Matrix = []
        for i in range(width):
            Matrix.append([fill]*height)
        return Matrix

    def sigmoid(x):
        return math.tanh(x)

    def Predict(self, inputs):
        if len(inputs) != self.NumberInputs-1:
            raise ValueError('wrong number of inputs')

        for i in range(self.NumberInputs-1):
            #self.ai[i] = sigmoid(inputs[i])
            self.ValuesInputNeurons[i] = inputs[i]

        for j in range(self.NumberHiddenNeyrons):
            sum = 0.0
            for i in range(self.NumberInputs):
                sum = sum + self.ValuesInputNeurons[i] * self.InputWeights[i][j]
            self.ValuesHiddenNeurons[j] = sigmoid(sum)

        for k in range(self.NumberOutputs):
            sum = 0.0
            for j in range(self.NumberHiddenNeyrons):
                sum = sum + self.ValuesHiddenNeurons[j] * self.OutputWeights[j][k]
            self.ValuesOutputNeurons[k] = sigmoid(sum)

        return self.ValuesOutputNeurons[:]


    def SaveNeyro(self, FileName):
        File = open(FileName, "w")
        File.write(str(self.NumberInputs)+";")
        File.write(str(self.NumberHiddenNeyrons)+";")
        File.write(str(self.NumberHiddenNeyrons)+";")
        for i in xrange(self.NumberInputs):
            for j in xrange(self.NumberHiddenNeyrons):
                File.write(str(self.InputWeights[i][j])+";")
        for i in xrange(self.NumberHiddenNeyrons):
            for j in xrange(self.NumberOutputs):
                File.write(str(self.OutputWeights[i][j])+";")
        File.close()

    def LoadNeyro(self, FileName):
        File = open(FileName, "r")
        line = File.read()
        File.close()
        arr = string.split(line, ";")
        self.NumberInputs, self.NumberHiddenNeyrons, self.NumberOutputs = \
                                                int(arr[0]), int(arr[1]), int(arr[2])
        self.InputWeights = makeMatrix(self.NumberInputs, self.NumberHiddenNeyrons)
        self.OutputWeights = makeMatrix(self.NumberHiddenNeyrons, self.NumberOutputs)
        n = 2
        for i in xrange(self.NumberInputs):
            for j in xrange(self.NumberHiddenNeyrons):
                n += 1
                self.InputWeights[i][j] = float(arr[n])
        for i in xrange(self.NumberHiddenNeyrons):
            for j in xrange(self.NumberOutputs):
                n += 1
                self.OutputWeights[i][j] = float(arr[n])
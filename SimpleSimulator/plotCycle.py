from matplotlib import pyplot as plt
from progCounter import PC
import binConvertor

class plotter():
    cycleNo = 0
    xList = []
    yList = []
    pc = PC()

    def __init__(self, progCount):
        self.pc = progCount
        
    def update(self, ins):
        self.xList.append(self.cycleNo)
        self.yList.append(self.pc.COUNTER)
        opCode = binConvertor.binToInt(ins[:5])
        if opCode == 4 or opCode == 5:
            self.xList.append(self.cycleNo)
            self.yList.append(binConvertor.binToInt(ins[8:]))
        self.cycleNo += 1

    def plot(self):
        plt.scatter(self.xList,self.yList,color='#e63946',marker=".")
        plt.xlabel("Cycle Number")
        plt.ylabel("Memory Address Accessed")
        plt.title("Memory Address v/s Cycle Number")
        plt.show()
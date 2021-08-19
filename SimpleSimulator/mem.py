'''
Memory (MEM): MEM takes in an 8 bit address and returns a 16 bit value as the data.
The MEM stores 512bytes, initialized to 0s.

Functionality:

read/initialize: read (stdin) the bin file to memory.
getInst: get the current instruction for the program counter.
updateMem: update the memory address (if needed).
dump: dump the memory file in stdout.

Create a class.
'''
import sys
import binConvertor

class memHandler():
    mem = []
    MEM_SIZE = 256
    def __init__(self):
        for i in range(self.MEM_SIZE):
            self.mem.append('0000000000000000')

    def load(self,inputFile):
        for idx,line in enumerate(inputFile):
            self.mem[idx] = line.rstrip("\n")
    
    def getInst(self,progCount):
        return self.mem[progCount]

    def getValueAtAdd(self,memAdd):
        return binConvertor.binToInt(self.mem[memAdd])

    def loadValueAtAdd(self,memAdd,val):
        self.mem[memAdd] = binConvertor.intToBin(val)

    def update(self,memAdd,newVal):
        self.mem[memAdd] = binConvertor.intToBin(newVal,16)
    
    def dump(self):
        for memAdd in self.mem:
            sys.stdout.write(memAdd+'\n')

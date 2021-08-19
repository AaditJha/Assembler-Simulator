'''
Register File (RF): The RF takes in the register name (R0, R1, ... R6 or FLAGS) and
returns the value stored at that register.

Functionality

update(reg, regState): updates the state of register reg to regState
                        updates FLAGS register accordingly.
dump: dumps the register onto stdout as <R0><R1>.....<R6><FLAGS>

complete class definition
'''
import sys
import binConvertor

class registerFile():
    reg = [] #Store 7 values R0 - R6
    FLAGS = [] #Store 4 values V L G E
    
    def __init__(self):
        for i in range(7):
            self.reg.append(0)
        for i in range(4):
            self.FLAGS.append(0)
            
    def dumpFLAGS(self):
        sys.stdout.write('000000000000')
        for flag in self.FLAGS:
            sys.stdout.write(str(flag))
        sys.stdout.write('\n') 

    def dump(self):
        for _reg in self.reg:
            sys.stdout.write(binConvertor.intToBin(_reg,16) + ' ')
        self.dumpFLAGS()

    def updateReg(self,idx,val):
        #val is integer.
        self.reg[idx] = val
    
    def resetFLAGS(self):
        for i in range(4):
            self.FLAGS[i] = 0

    def updateFLAGS(self,idx):
        self.FLAGS[idx] = 1



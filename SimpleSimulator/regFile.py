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
    reg = [0]*7 #Store 7 values R0 - R6
    FLAGS = 0 # V = 8, L = 4, G = 2, E = 1
        

    def dump(self):
        for _reg in self.reg:
            sys.stdout.write(binConvertor.intToBin(_reg,16) + ' ')
        sys.stdout.write(binConvertor.intToBin(self.FLAGS,16) + '\n')

    def updateReg(self,idx,val):
        #val is integer.
        self.reg[idx] = val




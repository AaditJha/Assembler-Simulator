'''
Program Counter (PC): The PC is an 8 bit register which points to the current instruction.

Functionality

update: update PC accordingly
dump: print current PC_STATE as 8 bit binary
'''
import sys
import binConvertor

class PC():
    COUNTER = 0
    def __init__(self):
        self.COUNTER = 0
    
    def update(self,updateParam):
        if updateParam == -1:
            self.COUNTER += 1
        else:
            self.COUNTER = updateParam
    
    def dump(self):
        sys.stdout.write(binConvertor.intToBin(self.COUNTER,8) + ' ')
        
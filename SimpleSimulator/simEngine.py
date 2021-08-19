'''
Execution Engine (EE): The EE takes the address of the instruction from the PC, uses it
to get the stored instruction from MEM, and executes the instruction by updating the RF
and PC.

Functionality

execute: execute the given instruction
update: call for various updates such as PC, MEM or RF

'''
from regFile import registerFile
import binConvertor

class ISA():
    opCodeSet = []
    binEncoding = []

    def __init__(self):
        self.opCodeSet = [0,0,1,2,3,3,0,2,1,1,0,0,0,2,2,4,4,4,4]
        self.binEncoding = [['u2','r','r','r'],['r','im'], ['u5','r','r'],
                            ['r','mem'],['u3','mem']]

    def addISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        perform reg[regA] = reg[regB]+reg[regC]
        update reg array
        return -1
        
        '''
        pass

    def subISA(self,paramList):
        pass

    def movIISA(self,paramList):
        '''
        paramList = [regA,immVal,reg array, FLAGS array]
        updates reg[regA] as immVal
        '''
        regIdx = paramList[0]
        paramList[2][regIdx] = paramList[1]
        return -1

    def movRISA(self,paramList):
        '''
        paramList = [regA,regB,reg array, FLAGS array]
        updates reg[regA] = reg[regB]
        '''
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        paramList[2][regAIdx] = paramList[2][regBIdx]
        return -1

    def ldISA(self,paramList):
        '''
        paramList = [regA,mem,memFile,reg array,FLAGS array]
        updates reg[regA] = getValueAtAdd(mem)
        '''
        regIdx = paramList[0]
        paramList[3][regIdx] = paramList[2].getValueAtAdd(paramList[1])
        return -1

    def stISA(self,paramList):
        '''
        paramList = [regA,mem,memFile,reg array,FLAGS array]
        updates loadValue(reg[regA])
        '''
        regIdx = paramList[0]
        regVal = paramList[3][regIdx]
        paramList[2].loadValueAtAdd(paramList[1],regVal)
        return -1
    
    def mulISA(self,paramList):
        pass

    def divISA(self,paramList):
        pass
    
    def rsISA(self,paramList):
        pass

    def lsISA(self,paramList):
        pass

    def xorISA(self,paramList):
        pass

    def orISA(self,paramList):
        pass 

    def andISA(self,paramList):
        pass

    def notISA(self,paramList):
        pass

    def cmpISA(self,paramList):
        pass

    def jmpISA(self,paramList):
        pass

    def jltISA(self,paramList):
        pass

    def jgtISA(self,paramList):
        pass

    def jeISA(self,paramList):
        pass

    funCallDict = {
        0:  addISA,
        1:  subISA,
        2:  movIISA,
        3:  movRISA,
        4:  ldISA,
        5:  stISA,
        6:  mulISA,
        7:  divISA,
        8:  rsISA,
        9:  lsISA,
        10: xorISA,
        11: orISA,
        12: andISA,
        13: notISA,
        14: cmpISA,
        15: jmpISA,
        16: jltISA,
        17: jgtISA,
        18: jeISA,
    }

class execRunner():
    regObj = registerFile()
    isa = ISA()

    def encode(self,opCodeIdx,inst,memFile):
        if(opCodeIdx == 19):
            return -1,True

        ptr = 5
        idx = self.isa.opCodeSet[opCodeIdx]
        param = []
        for instTyp in self.isa.binEncoding[idx]:
            if instTyp == 'r':
                regNo = binConvertor.binToInt(inst[ptr:ptr+3])
                if regNo != 7:
                    param.append(regNo)
                ptr += 3

            elif instTyp[0] == 'u':
                ptr += int(instTyp[1])

            elif instTyp == 'im':
                param.append(binConvertor.binToInt(inst[ptr:ptr+8]))
                ptr += 8
            
            else:
                param.append(binConvertor.binToInt(inst[ptr:ptr+8]))
                param.append(memFile)
        
        if(idx != 4):
            param.append(self.regObj.reg)
            param.append(self.regObj.FLAGS)

        newPC = self.isa.funCallDict[opCodeIdx](self,param)

        return newPC,False


    def execute(self,inst,memFile):
        # UPDATE REGISTERS AND MEMADD ACCORDINGLY
        halted = False
        opCodeIdx = binConvertor.binToInt(inst[:5])
        newPC,halted = self.encode(opCodeIdx,inst,memFile)
        self.regObj.dump()
        if(newPC != -1):
            newPC = binConvertor.intToBin(newPC,16)
        return newPC,halted

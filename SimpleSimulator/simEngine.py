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

def resetFLAG(FLAGS):
    for i in range(len(FLAGS)):
        FLAGS[i] = 0

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
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        regVal = paramList[3][regBIdx] + paramList[3][regCIdx]
        if regVal > 65535:
            regVal -= 65536
            paramList[4][0] = 1
        paramList[3][regAIdx] = regVal
        return -1

    def subISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        perform reg[regA] = reg[regB]-reg[regC] or 0 in case of underflow
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        if paramList[3][regCIdx] > paramList[3][regBIdx]:
            paramList[3][regAIdx] = 0
            paramList[4][0] = 1
        
        else:
            paramList[3][regAIdx] = paramList[3][regBIdx] - paramList[3][regCIdx]
        return -1

    def movIISA(self,paramList):
        '''
        paramList = [regA,immVal,reg array, FLAGS array]
        updates reg[regA] as immVal
        '''
        resetFLAG(paramList[3])
        regIdx = paramList[0]
        paramList[2][regIdx] = paramList[1]
        return -1

    def movRISA(self,paramList):
        '''
        paramList = [regA,regB,reg array, FLAGS array]
        updates reg[regA] = reg[regB]/ reg[regA] = FLAGS (incase regB == 7)
        '''
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        if (regBIdx != 7):
            paramList[2][regAIdx] = paramList[2][regBIdx]
        else:
            flagVal = ''.join(str(i) for i in paramList[3])
            paramList[2][regAIdx] = binConvertor.binToInt(flagVal)
        resetFLAG(paramList[3])
        return -1

    def ldISA(self,paramList):
        '''
        paramList = [regA,mem,memFile,reg array,FLAGS array]
        updates reg[regA] = getValueAtAdd(mem)
        '''
        resetFLAG(paramList[4])
        regIdx = paramList[0]
        paramList[3][regIdx] = paramList[2].getValueAtAdd(paramList[1])
        return -1

    def stISA(self,paramList):
        '''
        paramList = [regA,mem,memFile,reg array,FLAGS array]
        updates loadValue(reg[regA])
        '''
        resetFLAG(paramList[4])
        regIdx = paramList[0]
        regVal = paramList[3][regIdx]
        paramList[2].loadValueAtAdd(paramList[1],regVal)
        return -1
    
    def mulISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        perform reg[regA] = reg[regB]*reg[regC]
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        regVal = paramList[3][regBIdx]*paramList[3][regCIdx]
        if regVal > 65535:
            regVal -= 65536
            paramList[4][0] = 1
        paramList[3][regAIdx] = regVal
        return -1

    def divISA(self,paramList):
        '''
        paramList = [regA,regB,reg array,FLAGS array]
        updates reg[0] = regA // regB and reg[1] = regA % rebB
        '''
        resetFLAG(paramList[3])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        paramList[2][0] = paramList[2][regAIdx] // paramList[2][regBIdx]
        paramList[2][1] = paramList[2][regAIdx] % paramList[2][regBIdx]
        return -1
    
    def rsISA(self,paramList):
        '''
        paramList = [regA,imm val, reg array, FLAGS array]
        updates reg[regA] = reg[regA]>>imm
        '''
        resetFLAG(paramList[3])
        regAIdx = paramList[0]
        regVal = binConvertor.intToBin(paramList[2][regAIdx],16)
        shiftVal = paramList[1]
        regVal = '0'*shiftVal + regVal[:-1*shiftVal]
        paramList[2][regAIdx] = binConvertor.binToInt(regVal)
        return -1

    def lsISA(self,paramList):
        '''
        paramList = [regA,imm val, reg array, FLAGS array]
        updates reg[regA] = reg[regA]<<imm
        '''
        resetFLAG(paramList[3])
        regAIdx = paramList[0]
        regVal = binConvertor.intToBin(paramList[2][regAIdx],16)
        shiftVal = paramList[1]
        regVal = regVal[shiftVal:] + '0'*shiftVal
        paramList[2][regAIdx] = binConvertor.binToInt(regVal)
        return -1

    def xorISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        updates reg[regA] = reg[regB] ^ reg[regC]
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        regLVal = binConvertor.intToBin(paramList[3][regBIdx], 16)
        regRVal = binConvertor.intToBin(paramList[3][regCIdx], 16)
        regEVal = ''
        for i in range(16):
            regEVal += str(int(regLVal)^int(regRVal))
        paramList[3][regAIdx] = binConvertor.binToInt(regEVal)
        return -1

    def orISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        updates reg[regA] = reg[regB] | reg[regC]
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        regLVal = binConvertor.intToBin(paramList[3][regBIdx], 16)
        regRVal = binConvertor.intToBin(paramList[3][regCIdx], 16)
        regEVal = ''
        for i in range(16):
            regEVal += str(int(regLVal)|int(regRVal))
        paramList[3][regAIdx] = binConvertor.binToInt(regEVal)
        return -1

    def andISA(self,paramList):
        '''
        paramList = [regA,regB,regC,reg array, FLAGS array]
        updates reg[regA] = reg[regB] & reg[regC]
        '''
        resetFLAG(paramList[4])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regCIdx = paramList[2]
        regLVal = binConvertor.intToBin(paramList[3][regBIdx], 16)
        regRVal = binConvertor.intToBin(paramList[3][regCIdx], 16)
        regEVal = ''
        for i in range(16):
            regEVal += str(int(regLVal[i])&int(regRVal[i]))
        paramList[3][regAIdx] = binConvertor.binToInt(regEVal)
        return -1

    def notISA(self,paramList):
        '''
        paramList = [regA,regB,reg array,FLAGS array]
        updates reg[regA] = NOT reg[regB]
        '''
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regLVal = binConvertor.intToBin(paramList[2][regBIdx], 16)
        regVal = ''
        for i in range(16):
            if regLVal[i] == '1':
                regVal += '0'
            else:
                regVal += '1'
        paramList[2][regAIdx] = binConvertor.binToInt(regLVal)
        return -1

    def cmpISA(self,paramList):
        '''
        paramList = [regA,regB,reg array,FLAGS array]
        updates VLGE accordingly
        '''
        resetFLAG(paramList[3])
        regAIdx = paramList[0]
        regBIdx = paramList[1]
        regLVal = paramList[2][regAIdx]
        regRVal = paramList[2][regBIdx]
        if regLVal < regRVal:
            paramList[3][1] = 1
        elif regLVal > regRVal:
            paramList[3][2] = 1
        else:
            paramList[3][3] = 1
        return -1

    def jmpISA(self,paramList):
        '''
        paramList = [mem,FLAGS array]
        return mem
        '''
        resetFLAG(paramList[1])
        return paramList[0]

    def jltISA(self,paramList):
        '''
        paramList = [mem,FLAGS array]
        return mem if L is 1
        '''
        if paramList[1][1] == 1:
            resetFLAG(paramList[1])
            return paramList[0]
        resetFLAG(paramList[1])
        return -1

    def jgtISA(self,paramList):
        '''
        paramList = [mem,FLAGS array]
        return mem if G is 1
        '''
        if paramList[1][2] == 1:
            resetFLAG(paramList[1])
            return paramList[0]
        resetFLAG(paramList[1])
        return -1

    def jeISA(self,paramList):
        '''
        paramList = [mem,FLAGS array]
        return mem if E is 1
        '''
        if paramList[1][3] == 1:
            resetFLAG(paramList[1])
            return paramList[0]
        resetFLAG(paramList[1])
        return -1

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
                param.append(regNo)
                ptr += 3

            elif instTyp[0] == 'u':
                ptr += int(instTyp[1])

            elif instTyp == 'im':
                param.append(binConvertor.binToInt(inst[ptr:ptr+8]))
                ptr += 8
            
            else:
                param.append(binConvertor.binToInt(inst[ptr:ptr+8]))
                if(idx == 3):
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

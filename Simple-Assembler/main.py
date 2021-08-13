import sys
from collections import OrderedDict
#regList -> Mapping between opcode in decimal and Type (A as 0,B as 1,...)
hltCount=0
memAddDict = OrderedDict()

regList = {
    "add"  :0,
    "sub"  :0,
    "movI" :1,
    "movR" :2,
    "ld"   :3,
    "st"   :3,
    "mul"  :0,
    "div"  :2,
    "rs"   :1,
    "ls"   :1,
    "xor"  :0,
    "or"   :0,
    "and"  :0,
    "not"  :2,
    "cmp"  :2,
    "jmp"  :4,
    "jlt"  :4,
    "jgt"  :4,
    "je"   :4,
    "hlt"  :5
    }


binEncoding = [['u2','r','r','r'],['r','im'],
['u5','r','r'],['r','mem'],['u3','mem'],
['u11']]

def givBin(intVal,bitsize):
    intVal = int(intVal)
    binStr = str(bin(intVal))[2:]
    binStr = '0'*(bitsize - len(binStr)) + binStr
    return binStr

def genBin(typ, cmnd):
    opDec = list(regList.keys()).index(cmnd[0])
    opBin  = givBin(opDec,5)
    binOut = opBin
    instISA = binEncoding[typ]
    idx = 1
    for inst in instISA:
        if idx == len(cmnd) and typ != 5:
            print ("Syntax Error")
            return -1
        if inst == 'r':
            if(cmnd[idx] == "FLAGS" and typ==2 and idx==2):
                rBin = "111"
            else:
                print ("Illegal Flag Usage")
            if (cmnd[idx][0] == 'R') and cmnd[idx][1:].isdigit() and 0 <= int(cmnd[idx][1:]) <= 6:
                rBin = givBin(cmnd[idx][1:],3)
                binOut += rBin
            else:
                print("Typo Error")
                return -1

        elif inst == 'mem':
            try:
                addBin = givBin(memAddDict[cmnd[idx]],8)
                binOut += addBin
            except KeyError:
                print("Missing Variable/Label")
                return -1
            except:
                print ("General Syntax Error")
                return -1    
    
        elif inst == 'im':
            if not (cmnd[idx][1:].isdigit()):
                print("Immediate value not an integer")
                return -1
            if not (0 <= int(cmnd[idx][1:]) <= 255):
                print ("Immediate value not in range")    
                return -1
            imBin = givBin(cmnd[idx][1:],8)
            binOut += imBin
        
        elif inst[0] == 'u':
            idx -= 1
            bitSize = int(inst[1:])
            binOut += '0'*bitSize

        idx += 1
    if idx != len(cmnd):
        print ("Syntax Error")
        return -1
    return binOut

def getOpType(cmnd):
    if cmnd[0] == 'mov':
        if cmnd[2][0] == "$":
            cmnd[0] = 'movI'
            return regList["movI"]
        elif cmnd[2][0] == 'R' or cmnd[2] == 'FLAGS':
            cmnd[0] = 'movR'
            return regList["movR"]
        else:
            print ("Typo Error")
            return -1
    else:
        try: 
            return regList[cmnd[0]]
        except KeyError:
            print("Typo Error")
            return -1
        except:
            print("General Syntax Error")
            return -1

def gotError(cmndLine,lncount,lnNum):
    lnNo='at Line : '+ str(lnNum)
    if hltCount > 1:
        print(" Multiple hlt instructions", lnNo)
        return True
    if lncount >= 256:
        print("Total number of operations exceeded", lnNo)
        return True
    if cmndLine[0] == 'var' and lncount != 0:
        print("Invalid variable assignment", lnNo)
        return True
    if (cmndLine[0] == 'hlt' or len(cmndLine) > 1) :
        print ("Invalid use of hlt function", lnNo)
        return True
    return False
    

    


def readCmnd(cmndLine):
    '''
    take a string and return it after splitting making a list.
    '''
    return cmndLine.split()

def isValidMemAdd (memAdd):
    reservedKey = regList.keys()
    reservedKey.remove('movI')
    reservedKey.remove('movR')
    reservedKey.append('mov')
    reservedKey.append('FLAGS')
    for i in range (7):
        reservedKey.append('R'+str(i))
    return (memAdd not in reservedKey) and (not memAdd.isdigit()) and (memAdd not in memAddDict.keys())
    

def preProcess():
    '''
    check for errors
    label/variable address map
    return list of strings where each string is a line in asm code.
    in case of error, call errorHandler it will return -1.
    '''
    global hltCount
    inputCode = []
    lncount = 0
    # for line in sys.stdin:
    for lnNum,line in enumerate(sys.stdin):
        line = readCmnd(line)
        if len(line):
            if line[0] == 'hlt':
                hltCount += 1
            if gotError(line,lncount,lnNum):
                return -1
            
            if line[0] == 'var':
                if isValidMemAdd(line[1]):
                    memAddDict[line[1]] = -1
                    lncount -= 1
                else:
                    print("Variable Misuse")
                    return -1

            elif line[0][-1] == ':':
                if isValidMemAdd(line[0][:-1]):
                    memAddDict[line[0][:-1]] = lncount
                    inputCode.append(line[1:])
                else:
                    print("Label Misuse")
                    return -1

            else:
                inputCode.append(line)
            lncount += 1

    if inputCode[-1][0] != 'hlt' :
        print("Missing Halt Instruction")
        return -1
    


    varidx = 1
    for addKey in memAddDict.keys():
        if memAddDict[addKey] == -1:
            memAddDict[addKey] = varidx+lncount-1
            varidx += 1
    return inputCode

def writeBin(binOut):
    '''
    taking a string which is a new line of code and writing it in output file.
    '''
    sys.stdout.write(binOut+'\n')

def runAssembler(asmCode):
    for codeLine in asmCode:
        typ = getOpType(codeLine)
        if typ == -1:
            return 
        binOut = genBin(typ,codeLine)
        if binOut == -1:
            return 
        writeBin(binOut)

def main():
    asmCode = preProcess()
    if(asmCode != -1):
        runAssembler(asmCode)

if __name__ == "__main__":
    main()


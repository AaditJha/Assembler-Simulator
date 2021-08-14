import sys
from collections import OrderedDict


#global variables
hltCount=0
asmLnCount = 0
lnNo = ''
#OrderedDict that maps labels and variables to its corresponding address in preProcess()
memAddDict = OrderedDict()


#This is the color class for the colored output (for handling errors)
class bcol:
    cend = '\33[0m'
    cred = '\33[31m'
    cyel = '\33[33m'
    cblu = '\33[34m'


#regList is a dict mapping instructions to type (A=0, B=1,...)
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


#This is the ISA instruction format corresponding to type.
binEncoding = [['u2','r','r','r'],['r','im'],
['u5','r','r'],['r','mem'],['u3','mem'],
['u11']]


#Helper function for binary padding
def givBin(intVal,bitsize):
    intVal = int(intVal)
    binStr = str(bin(intVal))[2:]
    if bitsize > len(binStr):
        binStr = '0'*(bitsize - len(binStr)) + binStr
    else:
        binStr = binStr[(len(binStr) - bitsize):]
    return binStr
    

def isValidMemAdd (memAdd,chk):
    '''
    Checks if given label/variable:
        is not a reserved keyword (Instruction or register)
        is not purely numerical and does not contain special characters (other than _)
        is not an existing label/variable name
    '''
    reservedKey = list(regList.keys())
    reservedKey.remove('movI')
    reservedKey.remove('movR')
    reservedKey.append('mov')
    reservedKey.append('FLAGS')
    if(chk):
        reservedKey += list(memAddDict.keys())
    for i in range (7):
        reservedKey.append('R'+str(i))
    for ltr in memAdd:
        if not ltr.isdigit() and (not(('a' <= ltr <= 'z') or ('A' <= ltr <= 'Z') or (ltr == '_'))):
            return False
    return (memAdd not in reservedKey) and (not memAdd.isdigit())


def genBin(typ, cmnd):
    '''
    Converts a given instruction into binary.
    Handles syntax error and illegal flag usage
    Returns a string that is the binary of a given instruction in cmnd
    '''
    errLine = "Instruction: "+bcol.cblu+" ".join(str(x) for x in cmnd)+bcol.cend
    errLine = errLine.replace("movR","mov")
    errLine = errLine.replace("movI","mov")
    opDec = list(regList.keys()).index(cmnd[0])
    opBin  = givBin(opDec,5)
    binOut = opBin
    instISA = binEncoding[typ]
    idx = 1
    
    for inst in instISA:
        if idx == len(cmnd) and typ != 5:
            print(bcol.cred+"Syntax Error"+bcol.cend,lnNo)
            print(errLine)
            return -1

        if inst == 'r':

            if(cmnd[idx] == "FLAGS"):
                if(typ==2 and idx==2):
                    rBin = "111"
                    binOut += rBin
                else:
                    print(bcol.cred+"Illegal Flag Usage"+bcol.cend,lnNo)
                    print(errLine)
                    return -1

            elif (cmnd[idx][0] == 'R') and cmnd[idx][1:].isdigit() and 0 <= int(cmnd[idx][1:]) <= 6:
                rBin = givBin(cmnd[idx][1:],3)
                binOut += rBin

            else:
                print(bcol.cred+"Invalid Register Type"+bcol.cend,lnNo)
                print(errLine)
                return -1

        elif inst == 'mem':
            if not(isValidMemAdd(cmnd[idx],False)):
                print(bcol.cred+"Illegal Memory Address"+bcol.cend,lnNo)
                print(errLine)
                print(bcol.cyel+"Note: Memory Address can't be reserved keywords/numerical."+bcol.cend)
                return -1
            try:
                addBin = givBin(memAddDict[cmnd[idx]],8)
                binOut += addBin
            except KeyError:
                print(bcol.cred+"Missing Variable/Label"+bcol.cend,lnNo)
                print(errLine)
                return -1
            except:
                print(bcol.cred+"General Syntax Error"+bcol.cend,lnNo)
                print(errLine)
                return -1    
    
        elif inst == 'im':

            if not (cmnd[idx][1:].isdigit()):
                print(bcol.cred+"Invalid Immediate Value"+bcol.cend,lnNo)
                print(errLine)
                print(bcol.cyel+"Note: Immediate Value must be an integer and in range [0,255]."+bcol.cend)
                return -1

            if not (0 <= int(cmnd[idx][1:]) <= 255):
                print(bcol.cred+"Invalid Immediate Value"+bcol.cend,lnNo)    
                print(errLine)
                print(bcol.cyel+"Note: Immediate Value must be an integer and in range [0,255]."+bcol.cend)
                return -1
            imBin = givBin(cmnd[idx][1:],8)
            binOut += imBin
        
        elif inst[0] == 'u':
            idx -= 1
            bitSize = int(inst[1:])
            binOut += '0'*bitSize

        idx += 1

    if idx != len(cmnd):
        print(bcol.cred+"Syntax Error"+bcol.cend,lnNo)
        print(errLine)
        return -1

    return binOut


def getOpType(cmnd):
    '''
    Returns the type of instruction from the given instruction
    Else prints an error and returns -1
    '''
    errLine = "Instruction: "+bcol.cblu+" ".join(str(x) for x in cmnd)+bcol.cend
    if cmnd[0] == 'mov':
        if cmnd[2][0] == "$":
            cmnd[0] = 'movI'
            return regList["movI"]
        elif cmnd[2][0] == 'R' or cmnd[2] == 'FLAGS':
            cmnd[0] = 'movR'
            return regList["movR"]
        else:
            print(bcol.cred+"Invalid Instruction "+bcol.cend,lnNo)
            print(errLine)
            return -1
    else:
        try: 
            return regList[cmnd[0]]
        except KeyError:
            print(bcol.cred+"Typo Error"+bcol.cend,lnNo)
            print(errLine)
            return -1
        except:
            print(bcol.cred+"General Syntax Error"+bcol.cend,lnNo)
            print(errLine)
            return -1


def gotError(cmndLine,lncount):
    '''
    Handles if:
        there are multiple hlt instructions
        number of operations exceeds 256
        initialize a variable not at the starting of the code
        hlt used incorrectly
    '''
    errLine = "Instruction: "+bcol.cblu+" ".join(str(x) for x in cmndLine)+bcol.cend
    if hltCount > 1:
        print(bcol.cred+"Multiple hlt instructions"+bcol.cend, lnNo)
        print(errLine)
        return True
    if lncount >= 256:
        print(bcol.cred+"Total number of operations exceeded"+bcol.cend, lnNo)
        print(errLine)
        return True
    if cmndLine[0] == 'var' and lncount != 0:
        print(bcol.cred+"Invalid variable assignment"+bcol.cend, lnNo)
        print(errLine)
        return True
    if (cmndLine[0] == 'hlt' and len(cmndLine) > 1) :
        print(bcol.cred+"Invalid use of hlt function"+bcol.cend, lnNo)
        print(errLine)
        return True
    return False
    

#Wrapper function to convert a string into a list of strings after stripping whitespaces
def readCmnd(cmndLine):
    return cmndLine.split()
    

def preProcess():
    '''
    Sanitizing input 
    Checking for valid labels and variables and hlt instruction
    Updating memAddDict accordingly
    Returns inputCode (A list of strings where each string is a sanitized instruction)
    Returns -1 if it encounters some error (does not include all errors, they are checked elsewhere)
    '''
    global hltCount
    inputCode = []
    lncount = 0
    for line in sys.stdin:
        line = readCmnd(line)
        errLine = "Instruction: "+bcol.cblu+" ".join(str(x) for x in line)+bcol.cend
        if len(line):

            if line[0] == 'hlt':
                hltCount += 1

            if gotError(line,lncount): #Checking for basic errors
                return -1
            
            if line[0] == 'var':
                if isValidMemAdd(line[1],True):
                    memAddDict[line[1]] = -1
                    lncount -= 1
                else:
                    print(bcol.cred+"Illegal Variable Assignment"+bcol.cend,lnNo)
                    print(errLine)
                    print(bcol.cyel+"Note: Variables can't be reserved keywords/numerical or existing labels/variables."+bcol.cend)
                    return -1

            elif line[0][-1] == ':':
                if isValidMemAdd(line[0][:-1],True):
                    memAddDict[line[0][:-1]] = lncount
                    inputCode.append(line[1:])
                else:
                    print(bcol.cred+"Illegal Label Assignment"+bcol.cend,lnNo)
                    print(errLine)
                    print(bcol.cyel+"Note: Labels can't be reserved keywords/numerical or existing labels/variables."+bcol.cend)
                    return -1

            else:
                inputCode.append(line)
            lncount += 1
    
    if len(inputCode) == 0:
        return -1
        
    if inputCode[-1][0] != 'hlt' :
        print(bcol.cred+"Missing Halt Instruction"+bcol.cend,errLine,bcol.cyel+"Note: Last instruction must be hlt."+bcol.cend, sep='\n')
        return -1
    
    #Updating the memAddDict
    varidx = 0
    for addKey in memAddDict.keys():
        if memAddDict[addKey] == -1:    #Checking for variable names
            memAddDict[addKey] = varidx+lncount  #Assigning a memory address to corresponding variable after all instructions are read
            varidx += 1
    return inputCode


#Wrapper function to print bin output in stdout
def writeBin(binOut):
    sys.stdout.write(binOut + '\n')


def runAssembler(asmCode):
    global lnNo
    global asmLnCount
    for codeLine in asmCode:    #Interpreting instructions
        typ = getOpType(codeLine)
        if typ == -1:
            return 
        binOut = genBin(typ,codeLine)
        if binOut == -1:
            return 
        writeBin(binOut)
        asmLnCount += 1
        lnNo = 'At Instruction: ' + str(asmLnCount)


def main():
    asmCode = preProcess()
    if (asmCode != -1):  #Checking if encountered an error in preProcess.
        runAssembler(asmCode)


#Driver code
if __name__ == "__main__":
    main()


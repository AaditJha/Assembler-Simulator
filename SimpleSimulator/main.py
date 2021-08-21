'''
Main Simulator File
'''
import sys
from mem import memHandler
from progCounter import PC
from simEngine import execRunner

sim = execRunner()
memFile = memHandler()
memFile.load(sys.stdin)
pc = PC()
halted = False

while(not halted):
    newInstruction = memFile.getInst(pc.COUNTER)
    pc.dump()
    newPC, halted = sim.execute(newInstruction,memFile)
    pc.update(newPC)
memFile.dump()
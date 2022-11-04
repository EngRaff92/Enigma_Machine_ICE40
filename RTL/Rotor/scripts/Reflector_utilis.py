###################
## MAIN PACKAGES 
###################
from path_locator_lib import *
from pyModel.Reflector import Reflector
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time

###################
## MAIN REFLECTORS
###################
Reflectors = {
    "A"     : "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B"     : "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C"     : "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    "ETW"   : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "UKW"   : "QYHOGNECVPUZTFDJAXWMKISRBL" 
}

###################
## ROUTINES     
###################
## convert
def convert(l: str)-> int:
    '''
        utility to convert the given letter to a number from 0-26
    '''
    return ord(l) - ord("A")

## genImage
def genImage(reflector: list):
    '''
        utility to Generate a reflector Binary file to be loaded into the LUT
    '''    
    file= pcollateral+"./reflector.bin"
    cmd = "rm -rf {}".format(file)    
    ## Execute
    if(os.path.exists(file)):
        os.system(cmd)
    with open(file, 'w') as f:
        for c in reflector:
            ## 5 bits in total, no flag just the output letter
            f.write("0b{:05b}\n".format(convert(c)).replace("0b",""))

## getTestName
def getTestName()-> str:
    '''
        utility that returns the test name
    '''
    from cocotb import regression_manager as rgm
    return rgm._test.name

## getValue
def getValue(flag: int, char: str)-> int:
    '''
        utility that returns the value in INT correspodning to a flag and a CHAR
    '''
    return int("0b"+str(flag)+"0b{:05b}".format(convert(char)).replace("0b",""),2)
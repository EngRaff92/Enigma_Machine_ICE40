###################
## MAIN PACKAGES 
###################
from cocotb.triggers    import Timer
from cocotb.utils       import get_sim_time
from cocotb.result      import TestFailure
from cocotb.binary      import BinaryValue

###################
## PATH LOCATOR
###################
from path_locator_lib import *
import pyModel.Plugboard as pbfile

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
def genImage(plugs: dict):
    '''
        utility to Generate a plugboard Binary file to be loaded into the LUT
    '''    
    file= pcollateral+"/plugboard.bin"
    cmd = "rm -rf {}".format(file)    
    ## RUN
    if(os.path.exists(file)):
        os.system(cmd)
    with open(file, 'w') as f:
        for c in plugs.keys():
            ## 6 bits in total
            ## ---- 5 ----- 4 --------- 0
            ##      |       |           |
            ## plugged flag     Plug     
            f.write(str(plugs[c][0])+"0b{:05b}\n".format(convert(plugs[c][1])).replace("0b",""))

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
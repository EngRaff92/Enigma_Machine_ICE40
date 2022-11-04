###################
## MAIN PACKAGES 
###################
from path_locator_lib import *
from cocotb.triggers import Timer
from random import randrange
from Env_Settings import *

###################
## ROUTINES     
###################
## genImage
def genImage(range_looping: int):
    '''
        utility to Generate a Binary file to be loaded into the LUT
    '''    
    file= pcollateral+"/mem.hex"
    cmd = "rm -rf {}".format(file)    
    ## Execute
    if(os.path.exists(file)):
        os.system(cmd)
    with open(file, 'w') as f:
            for n in range(range_looping):
                f.write("{}\n".format(hex(randrange(0,2**range_looping-1)).replace("0x","")))

## getTestName
def getTestName()-> str:
    '''
        utility that returns the test name
    '''
    from cocotb import regression_manager as rgm
    return rgm._test.name
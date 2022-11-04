###################
## PATH LOCATOR
###################
import os
import sys
cwd     = os.path.dirname(os.path.realpath(__file__))  ## SCRIPTS
pwd     = os.path.dirname(cwd)                         ## ../
ppwd    = os.path.dirname(pwd)                         ## ../
pppwd   = os.path.dirname(ppwd)                        ## ENIGMA_ICE40
sys.path.append(pwd)
sys.path.append(pppwd)
from Env_Settings import *
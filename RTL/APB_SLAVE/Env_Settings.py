'''
    File used to share all the configuration objects across multiple files
    It contains the internal path for Design and Verification.
    It is highly sharable since all the path are computed from the PWD
'''

##############################
## SETTING PATHS
##############################
import os
import sys
import glob as g
import cocotb

## Set internal paths
pwd         = os.path.dirname(os.path.realpath(__file__)) 
prtl        = pwd+"/rtl/"
psim        = pwd+"/sim/"
pscritps    = pwd+"/scripts/"
pbuild      = pwd+"/sim_build/"
pcollateral = pwd+"/collateral/"
pmodel      = pwd+"../../pyModel/"

## SET to python
sys.path    += [pwd,prtl,psim,pscritps,pmodel,pcollateral]

##############################
## Pytest configuration
##############################
envSIM              = os.getenv('SIM')
if(envSIM == "icarus"):
    simulator       = "icarus",
    compile_args    = ["-g2012"]
    extraArgs       = []
elif(envSIM == "verilator"):
    simulator       = "verilator"
    compile_args    = [ "-Wno-UNOPTFLAT","-Wno-TIMESCALEMOD","--exe","--trace",
                        "--trace-depth 10000","--trace-structs","--trace-fst",
                        "--trace-max-array 10000","--trace-max-width 10000"]
    extraArgs       = ["--trace-fst","--trace-structs","--Wno-UNOPTFLAT","--Wno-REDEFMACRO"]
    covereageArgs   = ["--coverage","--coverage-line","--coverage-toggle"]
else:
    assert 0, "Error simulator is not set"

## Set module name
module_name         = os.getenv("DUT")

##############################
## Simulation configuration
##############################
estra_options   = {
    'COCOTB_HDL_TIMEUNIT'       : os.getenv("TIMEUNIT"),
    'COCOTB_HDL_TIMEPRECISION'  : os.getenv("TIMEPREC")
}
fileSource      = list(g.glob(f'{prtl}**/*.sv',recursive=True))

##############################
## DUT configuration
##############################
param_DATA_WIDTH    = "32" 
param_ADDR_WIDTH    = "5"  
param_IMAGE         = '\"{}\"'.format(pcollateral+"/mem.hex")
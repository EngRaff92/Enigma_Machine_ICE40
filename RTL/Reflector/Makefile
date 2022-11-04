###########################################################################
### MAKEFILE REFLECTOR													###
###########################################################################
TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
PYTHON=python3.9
filename=reflector
COCOTB_HDL_TIMEPRECISION=1ns
COCOTB_HDL_TIMEUNIT=1ns
COCOTB_LOG_LEVEL=

## Export the simulator
export SIM=icarus
export DUT=${filename}
export TIMEUNIT=1ns
export TIMEPREC=1ps
export TOPLEVEL=${filename}

## Include Submodules Like python Model
export PYTHONPATH=${PWD}/pyModel

## Set the RUNDIR as main folder
export RUN_DIR=$(shell pwd)

## Include COCOTB
include $(shell cocotb-config --makefiles)/Makefile.sim

###########
## RULES ##
###########
.PHONY: clean_all createitems run_${filename}

createitems:
	@$(PYTHON) ${PWD}/scripts/CreateReflector.py A

clean_all: 
	@rm -rf ./sim_build
	@rm -rf __pycache__
	@rm -rf ./scripts/__pycache__
	@rm -rf ./sim/__pycache__
	@rm -rf ${PWD}/collateral/*.hex 
	@rm -rf ${PWD}/collateral/*.bin
	@rm -rf ./.pytest_cache

run_${filename}: createitems
	@make TOPLEVEL=${filename} MODULE=test_${filename}
	
run_all: clean_all createitems
	${shell source ./scripts/run_pytest.sh}

runys_${filename}: createitems
	@yosys ./run_yosys.ys

build_ice40_${filename}: createitems
	@yosys -l ./yosys.log -p "read_verilog -sv ${PWD}/rtl/$(filename).sv; show -prefix view_file -notitle -colors 2 -width -format dot; synth_ice40 -top $(filename) -json ${PWD}/collateral/result.json; write_verilog -sv ${PWD}/collateral/$(filename)_synth.sv"
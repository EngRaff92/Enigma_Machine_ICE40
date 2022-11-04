###########################################################################
### MAKEFILE PLUGBOARD													###
###########################################################################
TOPLEVEL_LANG ?= verilog
PWD=$(shell pwd)
VERILOG_SOURCES=$(PWD)/plugboard.sv
PYTHON=python3.9
filename=plugboard
COCOTB_HDL_TIMEPRECISION=1ns
COCOTB_HDL_TIMEUNIT=1ns
COCOTB_LOG_LEVEL=

## Export the simulator
export SIM=icarus
export DUT=plugboard
export TIMEUNIT=1ns
export TIMEPREC=1ps
export TOPLEVEL=plugboard

## Include Submodules Like python Model
export PYTHONPATH=${PWD}/pyModel

## Set the RUNDIR as main folder
export RUN_DIR=$(shell pwd)

## Include COCOTB
include $(shell cocotb-config --makefiles)/Makefile.sim

###########
## RULES ##
###########
.PHONY: clean_all createplug run_debug_plugboard run_plugboard runys_plugboard build_ice40_plugboard

createplug:
	@$(PYTHON) ./scripts/CreatePlug.py

clean_all: 
	@rm -rf ./sim_build
	@rm -rf __pycache__
	@rm -rf ./scripts/__pycache__
	@rm -rf ./sim/__pycache__
	@rm -rf ${PWD}/collateral/plugboard.hex 
	@rm -rf ${PWD}/collateral/plugboard.bin
	@rm -rf ./.pytest_cache

run_plugboard_random: createplug
	@make TOPLEVEL=plugboard MODULE=test_plugboard

run_plugboard_std: createplug
	@make TOPLEVEL=plugboard MODULE=test_plugboard_std_conf

run_plugboard_error: createplug
	@make TOPLEVEL=plugboard MODULE=test_plugboard_error

test_plugboard_error_overflow: createplug
	@make TOPLEVEL=plugboard MODULE=test_plugboard_error_overflow
	
run_all: clean_all createplug
	${shell source ./scripts/run_pytest.sh}

runys_plugboard: createplug
	@yosys ./run_yosys.ys

build_ice40_plugboard: createplug
	@yosys -l ./yosys.log -p "read_verilog -sv ./$(filename).sv; show -prefix view_file -notitle -colors 2 -width -format dot; synth_ice40 -top $(filename) -json result.json; write_verilog -sv $(filename)_synth.sv"
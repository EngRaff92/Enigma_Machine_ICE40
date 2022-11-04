## Fix eventually errors with PYTEST
unset PYTHONPATH
## Export the simulator
export SIM=icarus
export DUT=plugboard
export TIMEUNIT=1ns
export TIMEPREC=1ps
export TOPLEVEL=plugboard
## RUN
pytest --quiet --no-header --cache-clear --disable-warnings --log-file=./sim_build/sim.log ${PWD}/test_Pytest_Plugboard_testlist.py
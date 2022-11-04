## Fix eventually errors with PYTEST
unset PYTHONPATH
## Export the simulator
export SIM=icarus
export DUT=apb_slave_wrapper
export TIMEUNIT=1ns
export TIMEPREC=1ns
export TOPLEVEL=apb_slave_wrapper
## RUN
pytest --quiet --no-header --cache-clear --disable-warnings --log-file=./sim_build/sim.log ${PWD}/test_Pytest_${DUT}_testlist.py
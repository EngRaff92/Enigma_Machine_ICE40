###################
## IMPORT
###################
from Env_Settings import *
from cocotb_test.simulator import run
import pytest

##############################################################################
## TIPS
##############################################################################
"""
Use this to execute the test which will not be counted into the entire number of FAILING tests
@pytest.mark.xfail

Use this to just skip the execution of a specific test
@pytest.mark.skip

Use this to give a specific test method a name ID the exeucte it by using py.test -m ID_NAME
@pytest.mark.ID_NAME

Use this to give a specific test parameters to be used
@pytest.mark.parametrize("name1, name2",value_type_1, value_type_2)

If pip install pytest-sugar is ran then pytest is gonna likly execute a bar progression while
running tests (expecially if in Parallel)
"""

##############################################################################
## TESTS REFLECTOR
##############################################################################
@pytest.mark.parametrize("parameters", [{
    "FILE"          : param_FILE,
    "ALPHABET_LEN"  : param_ALPHABET_LEN,
    "PORTLEN"       : param_PORTLEN,
    "STATE"         : param_STATE}])
@pytest.mark.repeat(10)
def test_reflector(parameters,request):
    run(
        verilog_sources     = fileSource,
        toplevel            = module_name,
        module              = "test_reflector", 
        simulator           = simulator,
        verilog_compile_args= compile_args,    
        parameters          = parameters,
        extra_env           = parameters,          
        plus_args           = [],
        sim_build           = pbuild+"test_reflector--"+request.node.callspec.id.replace("parameters",""),
    )
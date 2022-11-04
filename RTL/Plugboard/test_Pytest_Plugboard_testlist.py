###################
## IMPORT
###################
from random                 import seed
from cocotb_test.simulator  import run
from Env_Settings           import *
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
## LOG generation
##############################################################################
@pytest.hookimpl(hookwrapper=True,tryfirst=True)
def pytest_runtest_setup(item):
    import os
    logging_plugin = item.config.pluginmanager.get_plugin("logging-plugin")
    logging_plugin.set_log_path(os.path.join(pbuild+item.name+"sim.log"))
    yield
    
##############################################################################
## TESTS PLUGBOARD
##############################################################################
## TESTS PLUGBOARD
@pytest.mark.parametrize("parameters", [{
    "SELFPLUGGED"   : param_SELFPLUGGED,
    "ALPHABET_LEN"  : param_ALPHABET_LEN,
    "PORTLEN"       : param_PORTLEN,},])
@pytest.mark.repeat(20)
def test_plugboard_random_configration(parameters,request):
    run(
        verilog_sources     = fileSource,
        toplevel            = module_name,
        module              = "test_plugboard", 
        simulator           = simulator,
        verilog_compile_args= compile_args,    
        parameters          = parameters,
        extra_env           = parameters,          
        plus_args           = [],
        sim_build           = pbuild+"test_plugboard_random_configration--"+request.node.callspec.id.replace("parameters",""),
    )

## TESTS PLUGBOARD
@pytest.mark.parametrize("parameters", [{
    "SELFPLUGGED"   : param_SELFPLUGGED,
    "ALPHABET_LEN"  : param_ALPHABET_LEN,
    "PORTLEN"       : param_PORTLEN,},])
@pytest.mark.repeat(20)    
def test_plugboard_standard_configuration(parameters,request):
    run(
        verilog_sources     = fileSource,
        toplevel            = module_name,
        module              = "test_plugboard_std_conf",  
        simulator           = simulator,
        verilog_compile_args= compile_args,
        parameters          = parameters,
        extra_env           = parameters,   
        plus_args           = [],
        # seed                = range(2),                
        sim_build           = pbuild+"test_plugboard_standard_configuration--"+request.node.callspec.id.replace("parameters",""),
    )

## TESTS PLUGBOARD
@pytest.mark.parametrize("parameters", [{
    "SELFPLUGGED"   : param_SELFPLUGGED,
    "ALPHABET_LEN"  : param_ALPHABET_LEN,
    "PORTLEN"       : param_PORTLEN,},])
@pytest.mark.repeat(20)    
def test_plugboard_error(parameters,request):
    run(
        verilog_sources     = fileSource,
        toplevel            = module_name,
        module              = "test_plugboard_error",  
        simulator           = simulator,
        verilog_compile_args= compile_args,
        parameters          = parameters,
        extra_env           = parameters,           
        plus_args           = [],
        # seed                = range(2),
        sim_build           = pbuild+"test_plugboard_error--"+request.node.callspec.id.replace("parameters",""),
    )

## TESTS PLUGBOARD
@pytest.mark.parametrize("parameters", [{
    "SELFPLUGGED"   : param_SELFPLUGGED,
    "ALPHABET_LEN"  : param_ALPHABET_LEN,
    "PORTLEN"       : param_PORTLEN,},])
@pytest.mark.repeat(20)    
def test_plugboard_error_overflow(parameters,request):
    run(
        verilog_sources     = fileSource,
        toplevel            = module_name,
        module              = "test_plugboard_error_overflow",
        simulator           = simulator,
        verilog_compile_args= compile_args,
        parameters          = parameters,
        extra_env           = parameters,           
        plus_args           = [],
        # seed                = range(2),        
        sim_build           = pbuild+"test_plugboard_error_overflow--"+request.node.callspec.id.replace("parameters",""),
    )
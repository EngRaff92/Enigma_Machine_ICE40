#!/opt/homebrew/bin/python3.9
## Main Packages
import pytest

## Enigma component
from Plugboard import *

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
## TESTS PLUGBOARD
##############################################################################

@pytest.mark.test_plugboard_print
def test_plugboard_print():
    KB = PlugBoard()
    print(KB)

@pytest.mark.test_plugboard_plug
def test_plugboard_plug():
    AlphaB  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    h1      = AlphaB[:len(AlphaB)//2]
    h2      = AlphaB[len(AlphaB)//2:]
    KB = PlugBoard()
    for ii in range(len(AlphaB)//2):
        KB.Plug(h1[ii],h2[ii])
        assert KB.ExecutePlug(h1[ii]) == h2[ii], "{} input litteral is not properly swapped {}".format(KB.ExecutePlug(h1[ii]),h2[ii])

@pytest.mark.test_plugboard_reset
def test_plugboard_reset():
    AlphaB  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    h1      = AlphaB[:len(AlphaB)//2]
    h2      = AlphaB[len(AlphaB)//2:]
    KB = PlugBoard()
    for ii in range(len(AlphaB)//2):
        KB.Plug(h2[ii],h1[ii])
        assert KB.ExecutePlug(h2[ii]) == h1[ii], "{} input litteral is not properly swapped {}".format(KB.ExecutePlug(h2[ii]),h1[ii])   
    KB.ResetPlug()
    for ii in AlphaB:
        assert KB.ExecutePlug(ii) == ii, "{} input litteral is not properly swapped {} after reset".format(KB.ExecutePlug(ii),ii)   

@pytest.mark.test_plugboard_random
def test_plugboard_random():
    KB = PlugBoard()
    KB.RandomPlug()
    result = KB.GetPlugs()
    for w1, w2 in result.items():
        assert w2[0] == 1, "After randomize connection in PlugBoard litteral {} is not wired".format(w2[1])
        assert KB.ExecutePlug(w1) == w2[1], "After randomize Littern input {} not return correct litteral".format(w1)
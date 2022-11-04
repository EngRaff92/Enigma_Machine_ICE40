###################
## IMPORT
###################
from PlughBoard_utilis import *
import random as rd

###################
## MAIN
###################
## RUN
@cocotb.test()
async def test_plugboard_error_overflow(dut):
    '''
        Test for plugboard
    '''
    cocotb.log.info("#### START {} #####".format(getTestName()))

    ## Function Utility to Backdoor loading the Memory
    def LoadLut(v: int, p: int):
        assert p < dut.ALPHABET_LEN.value, "LoadLut -- Debug Input position: {} cannot exceed: {}".format(p,dut.ALPHABET_LEN.value - 1)
        assert v < 2**(dut.PORTLEN.value+1), "LoadLut -- Debug Input value: {} cannot exceed: {}".format(v,2**(dut.PORTLEN.value+1) - 1)
        cocotb.log.debug("Loading Value: {} at position: {}".format(v,p))
        dut.lut_plug[p].setimmediatevalue(v)

    ## Generate Plug Board Configuration before running Test (STD plugboard configuration where all Letters are Plugged with themselves)
    PBmodel = pbfile.PlugBoard(False)
    StdPlug = PBmodel.GetPlugs()
    genImage(StdPlug)

    ## Choose a random number value to be set
    target = rd.randint(dut.ALPHABET_LEN.value,2**(dut.PORTLEN.value)-1)
    ## Choose a random number position to be corrupted
    tindex = rd.randint(0, dut.ALPHABET_LEN.value-1)
    cocotb.log.info("Value of index Overflow is:{} ".format(tindex))
    cocotb.log.info("Value of Value Overflow is:{} ".format(target))
    TestPass1 = True
    TestPass2 = True

    ## Load Memory
    for index,elem in enumerate(StdPlug.values()):
        LoadLut(getValue(elem[0],elem[1]),index)
    
    ## Print configuration
    cocotb.log.debug("Plugboard configuration {}".format(PBmodel.GetPlugs()))

    ## Print Memory Content
    await Timer(1,"step")
    for ii in range(dut.ALPHABET_LEN.value):
        cocotb.log.debug("Internal Memory Content at index:{} is: {}".format(ii,dut.lut_plug[ii].value))

    ## as inital value let's zeroing out all the input
    dut.input_letter.value  = 0
    dut.pb_cs_n.value       = 1

    ## Wait few ns
    await Timer(1,"ns")

    ## RUN
    ## Define signal name as string and play with random values
    for counter,i in enumerate(StdPlug.keys()):
        ## Set a plug
        if(counter == tindex):
            dut.input_letter.value = BinaryValue(value=target, n_bits=dut.PORTLEN.value)
            result = 0
        else:
            result = convert(PBmodel.ExecutePlug(i))
            dut.input_letter.value = convert(i)
        dut.pb_cs_n.value = 0
        ## Wait few ns
        await Timer(1,"ns")
        ## TEST
        try:
            assert dut.output_letter.value == result
        except AssertionError as ex:
            TestPass1 = False
            cocotb.log.debug("Mismatch at {}ns: Expected is {} value sampled is: {} while input is: {}".format(get_sim_time("ns"),bin(result),bin(dut.output_letter.value),bin(dut.input_letter.value)))
        try:    
            assert dut.error.value == int(counter == tindex)
        except AssertionError as ex:
            TestPass2 = False
            cocotb.log.info("Error mismatch received: {} expected: {}".format(dut.error.value,int(counter == index)))
        ## Restart   
        dut.pb_cs_n.value = 1
        await Timer(1,"ns")
    ## END
    if(TestPass1 == False):
        raise TestFailure("Test Failed for Value Mismatch")
    if(TestPass2 == False):
        raise TestFailure("Test Failed for Error Mismatch")
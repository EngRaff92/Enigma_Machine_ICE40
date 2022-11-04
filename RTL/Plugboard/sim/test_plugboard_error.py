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
async def test_plugboard_error(dut):
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

    ## Choose a random number position to be set to 1
    target = rd.randint(0, dut.ALPHABET_LEN.value-1)

    ## Load Memory
    for index,elem in enumerate(StdPlug.values()):
        if(index == target):
            cocotb.log.info("Target selected is {}".format(target))
            LoadLut(getValue(1,elem[1]),index)
        else:
            LoadLut(getValue(elem[0],elem[1]),index)
    
    ## Print configuration
    cocotb.log.debug("Plugboard configuration {}".format(PBmodel.GetPlugs()))

    ## Print Memory Content
    await Timer(1,"step")
    for i in range(dut.ALPHABET_LEN.value):
        cocotb.log.debug("Internal Memory Content at index:{} is: {}".format(i,dut.lut_plug[i].value))

    ## as inital value let's zeroing out all the input
    dut.input_letter.value  = 0
    dut.pb_cs_n.value       = 1

    ## Wait few ns
    await Timer(1,"ns")

    ## Define signal name as string and play with random values
    for counter,i in enumerate(StdPlug.keys()):
        ## Set a plug
        result = convert(PBmodel.ExecutePlug(i))
        dut.input_letter.value = convert(i)
        dut.pb_cs_n.value = 0
        ## Wait few ns
        await Timer(1,"ns")
        ## TEST
        if(counter == target):
            ## I'm expecting an error and the Output to be 0
            assert dut.output_letter.value == 0, "Mismatch at {}ns: Expected is 0 value sampled is: {} while input is: {}".format(get_sim_time("ns"),bin(dut.output_letter.value),bin(dut.input_letter.value))
            assert dut.error.value == 1, "Error not asserted when error is expected"   
        else:
            ## I'm not expecting an error and the Output to be the predicted one
            assert dut.output_letter.value == result, "Mismatch at {}ns: Expected is {} value sampled is: {} while input is: {}".format(get_sim_time("ns"),bin(result),bin(dut.output_letter.value),bin(dut.input_letter.value))
            assert dut.error.value == 0, "Error asserted when no error is expected"         
        ## Restart   
        dut.pb_cs_n.value = 1
        await Timer(1,"ns")

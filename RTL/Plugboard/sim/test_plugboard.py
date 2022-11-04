###################
## IMPORT
###################
from PlughBoard_utilis import *

###################
## MAIN
###################
## RUN
@cocotb.test()
async def test_plugboard(dut):
    '''
        Test for plugboard
    '''
    cocotb.log.info("#### START {} #####".format(getTestName()))

    ## Function Utility to Backdoor loading the memory
    def LoadLut(v: int, p: int):
        assert p < dut.ALPHABET_LEN.value, "LoadLut -- Debug Input position: {} cannot exceed: {}".format(p,dut.ALPHABET_LEN.value - 1)
        assert v < 2**(dut.PORTLEN.value+1), "LoadLut -- Debug Input value: {} cannot exceed: {}".format(v,2**(dut.PORTLEN.value+1) - 1)
        cocotb.log.debug("Loading Value: {} at position: {}".format(v,p))
        dut.lut_plug[p].setimmediatevalue(v)

    ## Generate Plug Board Configuration before running Test
    PBmodel = pbfile.PlugBoard(False)
    PBmodel.RandomPlug()
    RandomPlug = PBmodel.GetPlugs()
    genImage(RandomPlug)

    ## Load Memory
    for index,elem in enumerate(RandomPlug.values()):
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
    for i in RandomPlug.keys():
        ## Set a plug
        result = convert(PBmodel.ExecutePlug(i))
        dut.input_letter.value = convert(i)
        dut.pb_cs_n.value = 0
        ## Wait few ns
        await Timer(1,"ns")
        ## TEST
        assert dut.output_letter.value == result, "Mismatch at {}ns: Expected is {} value sampled is: {} while input is: {}".format(get_sim_time("ns"),bin(result),bin(dut.output_letter.value),bin(dut.input_letter.value))
        assert dut.error.value == 0, "Error asserted when no error is expected"     
        ## Restart   
        dut.pb_cs_n.value = 1
        await Timer(1,"ns")
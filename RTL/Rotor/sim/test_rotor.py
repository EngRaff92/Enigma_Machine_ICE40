###################
## IMPORT
###################
from Reflector_utilis import *

###################
## MAIN
###################
## RUN
@cocotb.test()
async def test_reflector(dut):
    '''
        Test for reflector
    '''
    cocotb.log.info("#### START {} #####".format(getTestName()))

    ## Function Utility to Backdoor loading the Memory
    def LoadLut(v: int, p: int):
        assert p < dut.ALPHABET_LEN.value, "LoadLut -- Debug Input position: {} cannot exceed: {}".format(p,dut.ALPHABET_LEN.value - 1)
        assert v < 2**(dut.PORTLEN.value+1), "LoadLut -- Debug Input value: {} cannot exceed: {}".format(v,2**(dut.PORTLEN.value+1) - 1)
        cocotb.log.debug("Loading Value: {} at position: {}".format(v,p))
        dut.lut_reflect[p].setimmediatevalue(v)

    ## Generate Plug Board Configuration before running Test (STD reflector configuration where all Letters are Plugged with themselves)
    REmodel = Reflector("A",Reflectors["A"])
    Setting = REmodel.GetRAlpha()
    genImage(Setting)

    ## Load Memory
    for list_index,elem in enumerate(Setting):
            LoadLut(convert(elem),list_index)
    
    ## Print configuration
    cocotb.log.debug("reflector configuration {}".format(REmodel))

    ## Print Memory Content
    await Timer(1,"step")
    for i in range(dut.ALPHABET_LEN.value):
        cocotb.log.debug("Internal Memory Content at index:{} is: {}".format(i,dut.lut_reflect[i].value))

    ## as inital value let's zeroing out all the input
    dut.input_letter.value  = 0
    dut.re_cs_n.value       = 1

    ## Wait few ns
    await Timer(1,"ns")

    ## Define signal name as string and play with random values
    for i in REmodel.Reference:
        ## Set a value
        result = convert(REmodel.Reflect(i))
        dut.input_letter.value = convert(i)
        dut.re_cs_n.value = 0
        ## Wait few ns
        await Timer(1,"ns")
        ## TEST
        ## I'm not expecting an error and the Output to be the predicted one
        assert dut.output_letter.value == result, "Mismatch at {}ns: Expected is {} value sampled is: {} while input is: {}".format(get_sim_time("ns"),bin(result),bin(dut.output_letter.value),bin(dut.input_letter.value))
        assert dut.error.value == 0, "Error asserted when no error is expected"         
        ## Restart   
        dut.re_cs_n.value = 1
        await Timer(1,"ns")

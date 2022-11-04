###################
## IMPORT
###################
from cocotb import *
from apb_slave_vip import *
from scripts.APB_utilis import *
from cocotb.utils import get_sim_time

###################
## MAIN
###################
# Generate Image for the internal ROM
genImage(int(param_DATA_WIDTH,10))

## RUN
@cocotb.test()
async def test_apb_slave_wrapper(dut):
    """Test for apb_slave_wrapper"""
    log.info("#### START {} #####".format(getTestName()))

    ## Function Utility to Backdoor loading the Memory
    def LoadLut(v: int, p: int):
        assert p < dut.u_rom.DEPTH.value, "LoadLut -- Debug Input position: {} cannot exceed: {}".format(p,dut.u_rom.DEPTH.value - 1)
        assert v < 2**(dut.u_rom.DATAW.value+1), "LoadLut -- Debug Input value: {} cannot exceed: {}".format(v,2**(dut.u_rom.DATAW.value+1) - 1)
        log.debug("Loading Value: {} at position: {}".format(v,p))
        dut.u_rom.MEMARRAY[p].setimmediatevalue(v)

    ## Declare Interface
    interface = APBProxy_if(param_DATA_WIDTH,param_ADDR_WIDTH)

    ## Start connections     
    interface.addSignals(dut.clock,"PCLK")
    interface.addSignals(dut.ares,"PRES") 
    interface.addSignals(dut.psel,"PSEL")
    interface.addSignals(dut.pwrite,"PWRITE")
    interface.addSignals(dut.penable,"PENABLE")
    interface.addSignals(dut.paddr,"PADDR")
    interface.addSignals(dut.pwdata,"PWDATA") 
    interface.addSignals(dut.prot,"PROTNS")
    interface.addSignals(dut.pstrb,"PSTRB") 
    interface.addSignals(dut.prdata,"PRDATA")
    interface.addSignals(dut.pslverror,"PSLVERR")
    interface.addSignals(dut.pready,"PREADY")

    ## Initialize Signals
    await interface.initSignals(0)

    ## Generate Reset
    await resetGen(dut.ares,5)

    ## Print Memory Content
    [log.debug("Internal Memory Content at index:{} is: {}".format(i,hex(dut.u_rom.MEMARRAY[i].value))) for i in range(dut.u_rom.DEPTH.value)]

    ## Run Clock and Wait
    await clockGen(dut.clock,10)
    await waitNcycles(dut.clock,3)

    ## Declare the Driver
    driver = APBDriver(interface, param_DATA_WIDTH, param_ADDR_WIDTH, False)
    [await driver.APBWrite(i,i) for i in range(dut.u_rom.DEPTH.value)]
    await waitNcycles(dut.clock,10)
    for i in range(dut.u_rom.DEPTH.value):
        result = await driver.APBRead(i)
        assert result == i, "{}ns: Mismatch after read -> Expected: {}, Read: {}".format(get_sim_time(),hex(i),hex(result))
    await waitNcycles(dut.clock,10)
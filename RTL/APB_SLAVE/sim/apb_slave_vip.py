"""
    APB slave VIP. Used as main checking mechanism and as main Stimulus generator.
    The VIP will only provide tasks and function along with checking mechanims.
    1 -> TRX generator (No PYUVM)
    2 -> Randomization features
    3 -> Protocol checking based on coros
"""

"""
    Package Imports
"""
from random import randrange
from cocotb import log
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.clock import Clock
from cocotb import start_soon
from cocotb.binary import BinaryValue

"""##############################################################################################################################"""
"""
    Exceptions used for INIT and Protocol Violation
"""
class ValueNone(Exception):
    """
        Exception raised for errors in case a Parameter is NONE.
        Attributes:
            VarName -- input Variable
    """
    def __init__(self, Context, VarName):
        self.message = "Context: {} -- Variable {} cannot be NONE type should be initialized".format(Context,VarName)
        super().__init__(self.message)

class ValueBeyondAllowed(Exception):
    """
        Exception raised for errors in case a Parameter is NONE.
        Attributes:
            VarName -- input Variable
    """
    def __init__(self, Context, VarName):
        self.message = "Context: {} -- Variable {} cannot exceed parameter value".format(Context,VarName)
        super().__init__(self.message)

class ValueNone(Exception):
    """
        Exception raised for errors in case a Parameter is NONE.
        Attributes:
            VarName -- input Variable
    """
    def __init__(self, Context, VarName):
        self.message = "Context: {} -- Variable {} cannot be NONE type should be initialized".format(Context,VarName)
        super().__init__(self.message)

class PSELguard(Exception):
    """
        Exception raised for errors in case a Parameter is NONE.
        Attributes:
            VarName -- input Variable
    """
    def __init__(self, Context, VarName):
        self.message = "Context: {} -- Variable {} cannot exceed parameter value".format(Context,VarName)
        super().__init__(self.message)

class PENABLEguard(Exception):
    """
        Exception raised for errors in case a Parameter is NONE.
        Attributes:
            VarName -- input Variable
    """
    def __init__(self, Context, VarName):
        self.message = "Context: {} -- Variable {} cannot exceed parameter value".format(Context,VarName)
        super().__init__(self.message)
        
"""##############################################################################################################################"""

"""##############################################################################################################################"""
class APBProxy_if(object):
    """APB Proxy Interface type used for the slave, it's a single point PINS collector"""
    def __init__(self, DataW=None, AddrW=None) -> None:
        from cocotb.handle import ModifiableObject
        if(DataW==None):
            raise ValueNone(__class__.__name__,"DataW")
        else:
            self.DataW = DataW
        if(AddrW==None):
            raise ValueNone(__class__.__name__,"AddrW")
        else:
            self.AddrW = AddrW
        ## internal DUT handle
        self.pSignals = []
        self.Recorder = {}

    async def waitRCycle(self):
        """Wait up a single single cycle based on the clock rising edge"""
        await RisingEdge(self.PCLK)

    async def waitFCycle(self):
        """Wait up a single single cycle based on the clock falling edge"""
        await FallingEdge(self.PCLK)        

    async def StartRecording_coro(self):
        """Coro used To record how a signal change over time"""
        while(1):
            await RisingEdge(self.PCLK)
            for elem in self.pSignals:
                self.Recorder[elem._name].append(elem.value)

    async def initSignals(self, v: int):
        """Initialize signals to a known value"""
        self.PSEL.setimmediatevalue(v)
        self.PRES.setimmediatevalue(v)
        self.PCLK.setimmediatevalue(v)
        self.PADDR.setimmediatevalue(v)
        self.PWDATA.setimmediatevalue(v)
        self.PROTNS.setimmediatevalue(v)
        self.PENABLE.setimmediatevalue(v)
        self.PWRITE.setimmediatevalue(v)
        self.PSTRB.setimmediatevalue(v)
        start_soon(self.StartRecording_coro())

    def addSignals(self,signal, attr_name: str):
        """Function used to Add a Signal Handle to the list and create a DUT name indipendent Attribute"""
        self.pSignals.append(signal)
        setattr(self, attr_name, signal)
        self.Recorder[signal._name] = []

class APBTrx_t(object):
    """APB Transaction type used for the slave"""
    def __init__(self, DataW=None, AddrW=None, SlvError_En=False) -> None:
        if(DataW==None):
            raise ValueNone(__class__.__name__,"DataW")
        else:
            self.DataW = DataW
        if(AddrW==None):
            raise ValueNone(__class__.__name__,"AddrW")
        else:
            self.AddrW = AddrW 
        self.SlvError_En    = SlvError_En
        ## Local Data element
        self.Error          = 0
        self.Rdata          = 0
        self.Wdata          = 0
        self.Addr           = 0

    def getRand(self):
        """
        Randomize returns and object type as APBTrx with internal Randomized:
        ADDR - DATA - RDATA - SLVERROR
        """
        self.Rdata  = 0
        self.Wdata  = randrange(0, 2**int(self.DataW,10)-1)
        self.Addr   = randrange(0, 2**(int(self.DataW,10).bit_length()-1))
        self.Error  = 0 if(self.SlvError_En == False) else randrange(0,1)

    def setAddr(self, Addr: int):
        """Setter methods used to lacally change the content of the TRX"""
        if(Addr > 2**(int(self.DataW,10).bit_length()-1)):
            raise ValueBeyondAllowed(__class__.__name__,"Addr")
        else:
            self.Addr = Addr

    def setWdata(self, Wdata: int):
        if(Wdata > 2**int(self.DataW,10)-1):
            raise ValueBeyondAllowed(__class__.__name__,"Wdata")
        else:
            self.Wdata = Wdata      
    
    def setRdata(self, Rdata: int):
        if(Rdata > 2**int(self.DataW,10)-1):
            raise ValueBeyondAllowed(__class__.__name__,"Rdata")
        else:
            self.Rdata = Rdata

class APBDriver(object):
    """APB Driver type used for the slave (it behaves as Master) should be part of a Singleton BFM type"""
    def __init__(self, pins: APBProxy_if, DataW=None, AddrW=None, SlvError_En=False) -> None:
        """Parameter Propagation"""
        if(DataW==None):
            raise ValueNone(__class__.__name__,"DataW")
        else:
            self.DataW = DataW
        if(AddrW==None):
            raise ValueNone(__class__.__name__,"AddrW")
        else:
            self.AddrW = AddrW 
        self.SlvError_En = SlvError_En
        self.pins        = pins
        
    async def APBWrite(self, target_addr, target_wdata):
        APBTRX = APBTrx_t(self.DataW, self.AddrW,self.SlvError_En)
        APBTRX.setAddr(target_addr)
        APBTRX.setWdata(target_wdata)
        await self.APBAtomic_write(target_addr,target_wdata)

    async def APBRead(self, target_addr) -> int:
        APBTRX = APBTrx_t(self.DataW, self.AddrW,self.SlvError_En)
        APBTRX.setAddr(target_addr)
        APBTRX.setRdata(await self.APBAtomic_Read(APBTRX.Addr))
        return APBTRX.Rdata

    async def R_APBWrite(self):
        APBTRX = APBTrx_t(self.DataW, self.AddrW,self.SlvError_En)
        APBTRX.getRand()
        await self.APBAtomic_write(APBTRX.Addr,APBTRX.Wdata)

    async def R_APBRead(self) -> int:
        APBTRX = APBTrx_t(self.DataW, self.AddrW,self.SlvError_En)
        APBTRX.getRand()
        APBTRX.setRdata(await self.APBAtomic_Read(APBTRX.Addr))
        return APBTRX.Rdata

    async def APBAtomic_Read(self, at) -> int:
        """
            MAIN Read operation for an APB Slave. It behaves as Master in this case.
            1.  If PSEL 0 the slave has not beeing selected yet hence we can select it first.
                    PSEL 0 -> 1 means the FSM was in IDLE is moving into SETUP with a transfer requested
                    PSEL is already 1 hence a new transfer can be requested since we are in trafsering mode (SETUP)
            2.  PADDR and PWRITE can now be set accordingly
        """
        await self.pins.waitRCycle()
        if(self.pins.PSEL.value in [0,None]):
            """No Transfer going in SETUP and Transfer"""
            self.pins.PSEL.value  = 1
        """setting ADDR and DATA during the SETUP PAHSE"""
        self.pins.PADDR.value     = at
        self.pins.PWRITE.value    = 0
        self.pins.PWDATA.value    = 0
        """setting PENABLE now the Slave FSM should be settling into ACCESS PHASE"""
        await self.pins.waitRCycle()
        self.pins.PENABLE.value   = 1
        """At this stage if PREADY is 1 the slave can fullfill the request 
        in the next PCLK cycle, othwerwise we have a WAIT state transfer"""
        await self.pins.waitRCycle()
        if(self.pins.PREADY.value == 0):
            from cocotb.triggers import RisingEdge
            await RisingEdge(self.pins.PREADY)
        """Return the Data and set everything to 0"""
        self.pins.PENABLE.value = self.pins.PADDR.value = self.pins.PSEL.value = self.pins.PWRITE.value = 0
        await self.pins.waitRCycle()
        return self.pins.PRDATA.value.integer

    async def APBAtomic_write(self, at, wd):
        """
            MAIN Read operation for an APB Slave. It behaves as Master in this case.
            1.  If PSEL 0 the slave has not beeing selected yet hence we can select it first.
                    PSEL 0 -> 1 means the FSM was in IDLE is moving into SETUP with a transfer requested
                    PSEL is already 1 hence a new transfer can be requested since we are in trafsering mode (SETUP)
            2.  PADDR and PWRITE can now be set accordingly
        """
        await self.pins.waitRCycle()
        if(self.pins.PSEL.value in [0,None]):
            """No Transfer going in SETUP and Transfer"""
            self.pins.PSEL.value  = 1
        """setting ADDR and DATA during the SETUP PAHSE"""
        self.pins.PADDR.value     = at
        self.pins.PWDATA.value    = wd
        self.pins.PWRITE.value    = 1
        """setting PENABLE now the Slave FSM should be settling into ACCESS PHASE"""
        await self.pins.waitRCycle()
        self.pins.PENABLE.value   = 1
        """At this stage if PREADY is 1 the slave can fullfill the request 
        in the next PCLK cycle, othwerwise we have a WAIT state transfer"""
        await self.pins.waitRCycle()
        if(self.pins.PREADY.value == 0):
            from cocotb.triggers import RisingEdge
            await RisingEdge(self.pins.PREADY)
        """Return the Data and set everything to 0"""
        self.pins.PENABLE.value = self.pins.PADDR.value = self.pins.PSEL.value = self.pins.PWRITE.value = 0
        
class APBMonitor(object):
    """APB Monitor type used for the slave (it behaves as Simple Monitoring) should be part of a Singleton BFM type"""
    def __init__(self, target) -> None:
        self.dut = target
        
    async def M_APBWrite(self):
        """APB monitor Write"""
        pass

    async def M_APBRead(self):
        """APB monitor Read"""
        pass

class APBProtocolGuard(object):
    """APB Protocol Checker behaves as Simple Protocol Checker should be part of a Singleton BFM type"""
    def __init__(self, _if_handle: APBProxy_if) -> None:
        self.inf = _if_handle
    
    def isChanged(self, signal) -> bool:
        if(signal._name in self.inf.Recorder.keys()):
            return self.inf.Recorder[signal._name][-1] != self.inf.Recorder[signal._name][-2]
        else:
            log.error("Signal: {} never recorded in Simulation".format(signal._name))
    
    def Past(self, signal) -> int:
        if(signal._name in self.inf.Recorder.keys()):
            return self.inf.Recorder[signal._name][-2]
        else:
            log.error("Signal: {} never recorded in Simulation".format(signal._name))

    def Sample(self, signal) -> int:
        if(signal._name in self.inf.Recorder.keys()):
            return self.inf.Recorder[signal._name][-1]
        else:
            log.error("Signal: {} never recorded in Simulation".format(signal._name))

    def farPast(self, signal, N: int) -> int:
        if(signal._name in self.inf.Recorder.keys()):
            return self.inf.Recorder[signal._name][-N]
        else:
            log.error("Signal: {} never recorded in Simulation".format(signal._name))
    
    def Stable(self, signal) -> bool:
        return not self.isChanged(signal)
        
class APB_bfm(object):
    """APB BFM is a singleton type containing Driver Monitor and Protocol Checker internally"""
    def __init__(self, target, interface: APBProxy_if) -> None:
        self.dut    = target
        self.pins   = interface
        self.Drv    = APBDriver()
        self.Mon    = APBMonitor()
        self.Guard  = APBProtocolGuard()

    def setIF(self, if_hanlde: APBProxy_if):
        self.pins = if_hanlde

    def getIF(self) -> APBProxy_if:
        return self.pins
"""##############################################################################################################################"""
"""##############################################################################################################################"""

async def clockGen(clock, period):
    """Clock Generator"""
    start_soon(Clock(clock, period, units='ns').start())

async def resetGen(reset, timeOn):
    """Reset Generator"""
    reset.setimmediatevalue(0)
    for i in range(timeOn):
        await wait1ns()
    reset.setimmediatevalue(1)
    await wait1ns()
    reset.setimmediatevalue(0)

async def waitNcycles(clock, ncycles):
    """Wait N number of clock cycles"""
    for jj in range(ncycles):
        await RisingEdge(clock)

async def getSignal(clk, signal):
    """Get Signal Value based on clock"""
    await RisingEdge(clk)
    return signal.value

async def isChanged(clk, signal) -> bool:
    """Check a signals has changed"""
    future  = await getSignal(clk, signal)
    past    = await getSignal(clk, signal)
    return future != past

async def signalRecorder_rising(signal, collection: list):
    """Recording function to be used as brick for assertion"""
    await RisingEdge(signal)
    collection.append(signal.value)

async def signalRecorder_falling(signal, collection: list):
    """Recording function to be used as brick for assertion"""
    await FallingEdge(signal)
    collection.append(signal.value) 

async def wait1ns():
    """Wait 1 ns of simulation time"""
    await Timer(1, units='ns')
    log.debug("Simulation time has advanced by 1 ns")

def signalRecorder(signal, collection: list):
    """Recording function to be used as brick for assertion"""
    collection.append(signal.value)
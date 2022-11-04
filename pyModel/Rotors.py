''' 
    The below Rotors are part of the JSON file
    ----------------------------------------------------------------
    Rotor #	ABCDEFGHIJKLMNOPQRSTUVWXYZ	Model           Number
    IC	    DMTWSILRUYQNKFEJCAZBPGXOHV	Commercial      Enigma A, B
    IIC	    HQZGPJTMOBLNCIFDYAWVEUSRKX	Commercial      Enigma A, B
    IIIC	UQNTLSZFMREHDPXKIBVYGJCWOA	Commercial      Enigma A, B
    IR	    JGDQOXUSCAMIFRVTPNEWKBLZYH	German Railway  (Rocket)
    IIR	    NTZPSFBOKMWRCJDIVLAEYUXHGQ	German Railway  (Rocket)
    IIIR	JVIUBHTCDYAKEQZPOSGXNRMWFL	German Railway  (Rocket)
    UKW	    QYHOGNECVPUZTFDJAXWMKISRBL	German Railway  (Rocket)
    ETWR	QWERTZUIOASDFGHJKPYXCVBNML	German Railway  (Rocket)
    ----------------------------------------------------------------
    ----------------------------------------------------------------
    The below Reflectors are part of the JSON file
    Reflector #     ABCDEFGHIJKLMNOPQRSTUVWXYZ
    Reflector A	    EJMZALYXVBWFCRQUONTSPIKHGD
    Reflector B	    YRUHQSLDPXNGOKMIEBFZCWVJAT
    Reflector C	    FVPJIAOYEDRZXWGCTKUQSBNMHL
    ETW	            ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ----------------------------------------------------------------    
'''

## Main Shuffle list routine
def RandList() ->list:
    '''
        utility to generate a random list of char out from the standard list
    '''    
    import random
    t = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(t)
    return t

## Main Random Letter setter
def RandChar() ->str:
    '''
        utility to generate a random Char from the standard list
    '''
    import random
    return random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

def ShiftList(n: int, Inlist: list) ->list:
    '''
        utility to shift the list down by a specific number
    '''    
    from collections import deque
    temp = deque(Inlist)
    temp.rotate(n)
    return temp

## convert
def convert(l: str)-> int:
    '''
        utility to convert the given letter to a number from 0-26
    '''
    return ord(l) - ord("A")

## convert
def ConverBack(l: int)-> str:
    '''
        utility to convert the given number to an ASCII symbol
    '''
    return chr(l+ord("A"))

## Main Class
class Rotor(object):
    '''
        __init__ override since we do need to configure the Reflector and initialize the Rotated state
        An override of __str__ instead will be needed since we wanna print the configuration of such Class.
    '''
    def __init__(self, name: int, state: str, notch: str, ring: str, KeyList_Out: list) -> None: 
        self.Name       = name
        self.Stepper    = 0
        self.RingSett   = convert(RandChar()) if(len(state) == 0) else convert(ring)
        self.Notch      = convert(RandChar()) if(len(notch) == 0) else convert(notch)
        self.StartState = convert(RandChar()) if(len(state) == 0) else convert(state)
        self.AlphaB_In  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.AlphaB_Out = RandList() if(len(KeyList_Out) == 0) else KeyList_Out
        ## Entering Wiring for the scrumbler, mapping the starting shifted alphabet to an input configuration
        self.FwdWiring  = dict(zip(ShiftList(-self.AlphaB_In.index(state),self.AlphaB_In),self.AlphaB_Out))
        self.Mod        = len(list(self.FwdWiring.keys()))
        self.Turnover   = (abs((convert(notch)+convert(ring)))%self.Mod)
        self.debug      = False
        assert name <= max([3,4,5,6,7,8]), "Rotor Number {} is beyond the allowed limit: {}".format(name,max([3,4,5,6,7,8]))
        assert name != 0, "Rotor Number is not allowed to be 0"
        assert list(self.FwdWiring.keys()).index(state) == 0, "Entering wiring not set to the Start State"

    ## Main encryption function
    def EncryptFWD(self, KeyIn: str) -> str:
        '''
            Standard Exncrypt method for the rotor
        '''
        # Check if the input exixts into the chosen aphabet
        assert KeyIn in self.AlphaB_In, "Key provided {} doesn't exist within the chosen alphabet".format(KeyIn)
        assert KeyIn in self.AlphaB_Out, "Key provided {} doesn't exist within the chosen Rotor".format(KeyIn)        
        # Step if needed, anyway step first and then encrypt
        self.StepToward()
        # Get offset and initial Key location. Everything could have be coded up in 1 line, adding variabled for debug
        KeyLoc              = convert(KeyIn)
        # We do not need the ring setting since it will only change the notch location for the rollover NewKeyLoc 
        # basically tells us how the input key will enter in the wiring
        # Step the aplhabet for the output and add the starting state as well (ideally this can be done with numbers)
        ShiftedAlpha_In     = ShiftList(-self.Stepper-self.StartState-self.RingSett,self.AlphaB_In)
        ShiftedAlpha_Out    = ShiftList(-self.Stepper-self.StartState-self.RingSett,self.AlphaB_Out)
        # Get the key from the Output Alphabet
        NewKey_FromAlphabet = ShiftedAlpha_Out[KeyLoc]
        # Compute the output
        NewOutIndex         = ShiftedAlpha_In.index(NewKey_FromAlphabet)
        KeyOut              = self.AlphaB_In[NewOutIndex]
        if(self.debug == True):
            ## Debug
            print("#######################################################")
            print("Rotor #:                 {}".format(self.Name))
            print("StartState:              {}".format(self.StartState))
            print("KeyIn:                   {}".format(KeyIn))
            print("KeyLoc:                  {}".format(KeyLoc))
            print("self.Stepper:            {}".format(self.Stepper)) 
            print("NewEnteringKey:          {}".format(ShiftedAlpha_In[KeyLoc]))
            print("NewKey_FromAlphabet:     {}".format(NewKey_FromAlphabet))
            print("NewOutIndex:             {}".format(NewOutIndex))
            print("KeyOut:                  {}".format(KeyOut))
            print("LIST REMAP:              {}".format("-".join(self.AlphaB_In)))
            print("LIST IN:                 {}".format("-".join(ShiftedAlpha_In)))
            print("LIST OUT:                {}".format("-".join(ShiftedAlpha_Out)))
            print("LIST REMAP:              {}".format("-".join(self.AlphaB_Out)))
            print("#######################################################")        
        return KeyOut

    ## Main encryption function
    def EncryptBWD(self, KeyIn: str) -> str:
        '''
            Standard Exncrypt method for the rotor
        '''
        # Check if the input exixts into the chosen aphabet
        assert KeyIn in self.AlphaB_In, "Key provided {} doesn't exist within the chosen alphabet".format(KeyIn)
        assert KeyIn in self.AlphaB_Out, "Key provided {} doesn't exist within the chosen Rotor".format(KeyIn)        
        # Step if needed, anyway step first and then encrypt but for Backward we do not press any KEY
        # Get offset and initial Key location. Everything could have be coded up in 1 line, adding variabled for debug
        KeyLoc              = convert(KeyIn)
        # Step the aplhabet for the output and add the starting state as well (ideally this can be done with numbers)
        ShiftedAlpha_In     = ShiftList(-self.Stepper-self.StartState-self.RingSett,self.AlphaB_In)
        ShiftedAlpha_Out    = ShiftList(-self.Stepper-self.StartState-self.RingSett,self.AlphaB_Out)
        # Get the key from the Output Alphabet
        NewKey_FromAlphabet = ShiftedAlpha_In[KeyLoc]
        # Compute the output
        NewOutIndex         = ShiftedAlpha_Out.index(NewKey_FromAlphabet)
        KeyOut              = self.AlphaB_In[NewOutIndex]
        if(self.debug == True):
            ## Debug
            print("#######################################################")
            print("Rotor #:                 {}".format(self.Name))
            print("StartState:              {}".format(self.StartState))
            print("KeyIn:                   {}".format(KeyIn))
            print("KeyLoc:                  {}".format(KeyLoc))
            print("self.Stepper:            {}".format(self.Stepper))
            print("NewEnteringKey:          {}".format(self.AlphaB_In[abs(KeyLoc-self.StartState)%self.Mod]))
            print("NewKey_FromAlphabet:     {}".format(NewKey_FromAlphabet))
            print("NewOutIndex:             {}".format(NewOutIndex))
            print("KeyOut:                  {}".format(KeyOut))
            print("LIST REMAP:              {}".format("-".join(self.AlphaB_In)))
            print("LIST IN:                 {}".format("-".join(ShiftedAlpha_In)))
            print("LIST OUT:                {}".format("-".join(ShiftedAlpha_Out)))
            print("LIST REMAP:              {}".format("-".join(self.AlphaB_Out)))
            print("#######################################################")        
        return KeyOut

    ## ResetRotor
    def ResetRotor(self):
        '''
            This function will just grab again the Start state previously set and will basically
            rearrange the internl Wiring as never used for any encryption ever 
        '''
        self.Stepper = 0

    ## JmpVal
    def JmpVal(self, end: str)-> int:
        '''
            utility to convert the given letters into a JUMP value
        '''
        return abs(self.StartState - convert(end))

    ## IsInTurnover
    def IsInTurnover(self) ->bool:
        '''
            Function check if the current Step Letter is uqual to the turnover letter
            by Stepp Letter we mean the at which tbe rotor is considering the initial state
            and the amount of rotation being performed. In nutshell is the letter give back by
            the 0 position.
        '''
        if(self.Stepper == self.Turnover):
            print("Rotor: {} is in RollOver updating stepper forward to {}".format(self.Name,self.Stepper))
            return True
        else:
            return False

    ## StepToward
    def StepToward(self):
        '''
            Standard function used to move the rotor if is in Turnover and incrementing
            the Notch value by 1. On top of that  the internal dictionary Map is changed
            to accomodate the new starting position now shifted by 1
        '''  
        # Increase always for rotor 1
        if((self.Name == 1)):
            self.Stepper += 1
        elif(self.IsInTurnover()):
            print("Update Steppper for Rotor: {} to {}".format(self.Name,self.Stepper))
            self.Stepper += 1
        # Reset
        if(self.Stepper%26 == 0):
            if(self.debug):
                print("Reset {} Steppper for Rotor: {}".format(self.Stepper%26 == 0,self.Name))
            self.Stepper = 0

    ## GetState
    def GetState(self) -> str:
        '''
            Function returns the Start state position
        '''
        return self.StartState

    ## GetNotch
    def GetNotch(self) -> str:
        '''
            Function returns the Notch position
        '''
        return self.Notch

    ## GetState
    def GetTurnover(self) -> int:
        '''
            Function returns the Turnover value
        '''
        return self.Turnover

    ## GetSteps
    def GetSteps(self) -> int:
        '''
            Function returns the Notch value, meaning the amount of steps done
        '''
        return self.Stepper

    ## GetConfig
    def GetConfig(self) -> dict:
        '''
            function returns the currect Configuration Alphabet Map,
            the dictionary made by the Middle Alphabet and the Outter one
        '''
        Out = {
            "Name": self.Name,
            "Starting_State": self.StartState,
            "Ring_Setting": self.RingSett,
            "Notch": self.Notch,
            "Steps": self.GetSteps()
        }
        return Out

    ## Override string method to customize the print on class object
    def __str__(self) -> str:
        '''
            Print out Rotor configuration
        '''
        return "Rotor#: {} \nState: \t{} \nTurn: \t{} \nForward \nInit: \t{} \nMap: \t{} \nTo: \t{} \nand Backward \nInit: \t{} \nMap: \t{} \nTo: \t{}".format(self.Name, \
        self.StartState,self.Turnover,\
        "".join(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),"".join(list(self.FwdWiring.keys())),"".join(list(self.FwdWiring.values())), \
        "".join(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")),"".join(list(self.FwdWiring.values())),"".join(list(self.FwdWiring.keys())))
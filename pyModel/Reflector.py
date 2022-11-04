'''
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

## Main Class
class Reflector(object):
    '''
        __init__ override since we do need to configure the Reflector and initialize the Reflection dictionary
        An override of __str__ instead will be needed since we wanna print the configuration of such Class.
    '''
    def __init__(self, state: str, RefList: list) -> None: 
        self.state = convert(state)
        if(len(RefList) == 0):
            if(state == ""):
                self.AlphaB  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            else:
                self.AlphaB = ShiftList(self.state,list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        else:
            if(state == ""):
                self.AlphaB  = RefList
            else:
                self.AlphaB = ShiftList(self.state,RefList)
        self.Reference  = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.debug      = False

    ## Main reflector function
    def Reflect(self, KeyIn: str) -> str:
        '''
            Standard Reflect method to wire up 2 letters,
            for any given Kye in it will return the opposite of the letter
            meaning the letter + offset 
            where offset is the len of the alpahbet - index of the key in
        '''
        # first off get the random wired letter
        KeyInPos = self.AlphaB.index(KeyIn)
        if(self.debug == True):
            print("#######################################################")
            print("KeyInPos : {}".format(KeyInPos))
            print("KeyIN    : {}".format(KeyIn))
            print("Reflector -- Receiving {} Returning {}".format(KeyIn,self.Reference[KeyInPos]))
            print("LIST IN:                 {}".format("-".join(self.Reference)))
            print("LIST OUT:                {}".format("-".join(self.AlphaB)))
            print("LIST REMAP:              {}".format("-".join(self.Reference)))
            print("#######################################################")
        # Second return the corresponded Key for a given reflected signal
        return self.Reference[KeyInPos]

    ## GetState
    def GetState(self) -> int:
        '''
            Function returns the set state
        '''
        return self.state

    ## GetRAlpha
    def GetRAlpha(self) -> list:
        '''
            function returns the currect Mapping 
        '''
        return self.AlphaB

    ## Override string method to customize the print on class object
    def __str__(self) -> str:
        '''
            Print out Reflector configuration
        '''
        return "Reflector Configuration\nState: \t{} \nMap: \t".format(self.state) + "".join(self.AlphaB)
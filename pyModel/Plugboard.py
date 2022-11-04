'''
'''

## Main Class
class PlugBoard(object):
    '''
        __init__ override since we do need to configure the Plugboard and initialize the connections
        except for the connection. An override of __str__ instead will be needed since
        we wanna print the configuration of such Class. The connection dictionary is made by a tuple as well,
        were 0 means not connected else 1 means plugged already
    '''
    def __init__(self, debug) -> None:
        self.connections = {
            "A":(0,"A"),
            "B":(0,"B"),
            "C":(0,"C"),
            "D":(0,"D"),
            "E":(0,"E"),
            "F":(0,"F"),
            "G":(0,"G"),
            "H":(0,"H"),
            "I":(0,"I"),
            "J":(0,"J"),
            "K":(0,"K"),
            "L":(0,"L"),
            "M":(0,"M"),
            "N":(0,"N"),
            "O":(0,"O"),
            "P":(0,"P"),
            "Q":(0,"Q"),
            "R":(0,"R"),
            "S":(0,"S"),
            "T":(0,"T"),
            "U":(0,"U"),
            "V":(0,"V"),
            "W":(0,"W"),
            "X":(0,"X"),
            "Y":(0,"Y"),
            "Z":(0,"Z")
        }
        self.AlphaB = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.debug  = debug

    ## Main connection function
    def Plug(self, KeyIn: str, KeyOut: str):
        '''
            Standard Plugging method to wire up 2 letters
        '''
        ## check if the key prrovided exists
        assert KeyIn in self.connections.keys(), "Error in PlugBoard class KeyIn {} doesn't exist".format(KeyIn)
        assert KeyOut in self.connections.keys(), "Error in PlugBoard class KeyOut {} doesn't exist".format(KeyOut)
        assert self.connections[KeyIn][0] == 0, "Error KeyIn {} already plugged with Key {} cannot be plugged again".format(KeyIn, self.connections[KeyIn][1])
        ## If all the above checks are passing 
        self.connections[KeyIn]=(1,KeyOut)
        self.connections[KeyOut]=(1,KeyIn)
        if(self.debug):
            print("plugging In: {} with Out {}".format(KeyIn,KeyOut))
    
    ## Random Plugboard configuration
    def RandomPlug(self):
        '''
            This function basically will randmly connect letters making sure there will 
            be no clash among them
        '''
        import random
        ## Reset the Alphabet
        self.ResetPlug()
        ## RANDOM connections
        Shuffled_alpha = self.AlphaB
        random.shuffle(Shuffled_alpha)
        # Cryptographically secure RNG
        CRNG = random.SystemRandom()
        ## An alphabet could be mabe by an even number of symbols so we always round it down in case
        l_l  = len(self.AlphaB)//2 if(len(self.AlphaB)%2 == 0) else round(len(self.AlphaB)//2-0.1)
        for index, KI in enumerate(self.connections.keys()):
            # Pick up randomly a Key
            KO = CRNG.choice(Shuffled_alpha)
            # Check if Key In is plugged in that case we give back controll to the loop
            # The order these 2 If Statements are used is crucial to avoid hangs
            if(self.connections[KI][0] == 1):
                continue            
            # check if the Key Out is already plugged
            if(self.connections[KO][0] == 1):
                # Keep picking up till we get a not plugged one
                while self.connections[KO][0] == 1:
                    KO = CRNG.choice(Shuffled_alpha)
            self.Plug(KI,KO)
            if(self.debug == True):
                print("index            {}".format(index))
                print("KI               {}".format(KI))
                print("KO               {}".format(KO))
                print("connected KO     {}".format(self.connections[KO][0]))
                print("connected KI     {}".format(self.connections[KI][0]))
                print("Limit            {}".format(l_l))            
                print("self.connections {}".format(self.connections))
        ## Check if any Key is connected to itself in that case we set the Plug Flag to 0
        for index, KI in enumerate(self.connections.keys()):
            if(self.connections[KI][1] == KI):
                self.connections[KI] = (0,KI)

    ## Reset Plugboard
    def ResetPlug(self):
        '''
            Anytime this function is called it immediately restore the Plugboad as it 
            is not used in the current configuration of enigma
        '''
        for el in self.AlphaB:
            self.connections[el]=(0,el)

    ## ExecutePlug
    def ExecutePlug(self, KeyIn) -> str:
        '''
            Given the letter input KeyIn it will provide the Key Out based on the plug
        '''
        if(self.debug == True):
            print("Plugboard FWD -- Returning : {}".format(self.connections[KeyIn][1]))
        return self.connections[KeyIn][1]

    ## ExecutePlugBack
    def ExecutePlugBack(self, KeyIn) -> str:
        '''
            Given the letter input KeyIn it will provide the Key Out based on the plug
        '''
        inv_dict = {v[1]: k for k, v in self.connections.items()}
        if(self.debug == True):
            print("Plugboard BWD -- Returning : {}".format(inv_dict[KeyIn]))
        return inv_dict[KeyIn]

    ## GetPlugs
    def GetPlugs(self) -> dict:
        '''
            function which returns the entire plugboard wiring
        '''
        return self.connections

    ## GetPairs
    def GetPairs(self) -> str:
        '''
            function returns the plugboard pair settings in a form like AB CD EF ...
        '''
        temp = [str(k)+str(v[1]) for k,v in self.connections.items()]
        return " ".join(temp)

    ## StandardPlug
    def StandardPlug(self):
        '''
            function used to create a standard connection kind of like the PB doesn't exists 
            in the enigma Machine
        '''
        for k in self.connections.keys():
            self.connections[k] = (1,k) 

    ## Override string method to customize the print on class object
    def __str__(self) -> str:
        '''
            Print out Plugboard configuration
        '''
        return "PlugBoard Configuration\n{}".format(self.GetPairs())
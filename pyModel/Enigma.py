## Main Components
from Plugboard  import *
from Reflector  import *
from Rotors     import *
from enum import Enum
## Main Action 
encryption = 0
decryption = 1

## Main Enigma Machine
class Enigma(object):
    def __init__(self, pb: PlugBoard, re: Reflector, r1: Rotor, r2: Rotor, r3: Rotor, debug: bool) -> None:
        self.PB = pb
        self.RE = re
        self.R1 = r1
        self.R2 = r2
        self.R3 = r3 
        self.CT = []
        self.PB.debug = debug
        self.RE.debug = debug
        self.R3.debug = debug
        self.R2.debug = debug
        self.R1.debug = debug
        self.debug    = debug

    def __str__(self) -> str:
        '''
            Print out Enigma Configuration configuration
        '''
        return "\n{} \n{} \n{} \n{} \n{}".format(self.PB,self.RE,self.R1,self.R2,self.R3)

    def Execute(self, action: int, MSG: str) -> str:
        '''
            General Encrypt method for Enigma, there is no Decrypt method the same one will 
            be used in both direction.
        ''' 
        ## Check operation
        assert action in [encryption,decryption], "Operation supported are only Encryption and Decryption"
        ## Generate the Graph for each iteraction
        from pyvis import network as nx
        # Generally Speaking a letter might be scrambled at least 9 times:
        # 1. Plugboard
        # 2. R1-2-3
        # 3. Reflector
        # 4. R3-2-1
        # 5. Plugboard 
        ## Always clear the Cypher Text beforehand 
        self.CT.clear()
        ## Start
        for lett in MSG:
            if lett != " ":
                signal = lett.upper()
                if(self.debug):
                    print("#######################################################")
                    print("Encrypting Letter: {}".format(signal))
                    print("#######################################################")
                g=nx.Network(height='400px', width='50%',heading='Encryption letter: {}'.format(signal),directed =True)
                g.add_node(0, label='Entering Letter: {}'.format(signal), title='Keyboard', group=1)
                signal = self.PB.ExecutePlug(signal)
                g.add_node(1, label='PB - FWD: {}'.format(signal), title='Plugboard', group=1)
                signal = self.R1.EncryptFWD(signal)
                g.add_node(2, label='R1 - FWD: {}'.format(signal), title='Rotor1', group=1)
                signal = self.R2.EncryptFWD(signal)
                g.add_node(3, label='R2 - FWD: {}'.format(signal), title='Rotor2', group=1)
                signal = self.R3.EncryptFWD(signal)
                g.add_node(4, label='R3 - FWD: {}'.format(signal), title='Rotor3', group=1)
                signal = self.RE.Reflect(signal)
                g.add_node(5, label='RE: {}'.format(signal), title='Reflector', group=1)
                signal = self.R3.EncryptBWD(signal)
                g.add_node(6, label='R3 - BWD: {}'.format(signal), title='Rotor3', group=1)
                signal = self.R2.EncryptBWD(signal)
                g.add_node(7, label='R2 - BWD: {}'.format(signal), title='Rotor2', group=1)
                signal = self.R1.EncryptBWD(signal)
                g.add_node(8, label='R1 - BWD: {}'.format(signal), title='Rotor1', group=1)
                signal = self.PB.ExecutePlugBack(signal)
                g.add_node(9, label='PB - BWD: {}'.format(signal), title='c', group=1)
                if(lett.isupper()):
                    self.CT.append(signal.upper())
                else:
                    self.CT.append(signal.lower())
            else:
                self.CT.append(lett)
            # populates the nodes and edges data structures
            for ll in range(9):
                if(ll < 9):
                    g.add_edge(ll,ll+1)
                else:
                    g.add_edge(ll,0)
            # Generate HTML
            if(action == encryption):
                g.show('EncryptionFlow_{}.html'.format(lett.upper()))
            else:
                g.show('DencryptionFlow_{}.html'.format(lett.upper()))
        return "".join(self.CT)
        
    def ResetEnigma(self):
        if(self.debug):
            print("ResetEngma Running ..")
        self.R1.ResetRotor()
        self.R2.ResetRotor()
        self.R3.ResetRotor()
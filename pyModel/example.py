## Additional PKG
import json as j
with open('/Volumes/My_Data/MY_SYSTEMVERILOG_UVM_PROJECTS/ENIGMA_ICE40/pyModel/Rotors_Config.json', 'r') as f:
    RotorConfig = j.load(f)
ROSCONFIG = RotorConfig["Rotors"]
RESCONFIG = RotorConfig["Reflectors"]

## Main Component
from Enigma import *

#############################################################################
## MAIN
#############################################################################
## Global debug
debug = False

## Pugboard configuration
PlugConf = ["bq","cr","di","ej","kw","mt","os","px","uz","gh"]

## Create classes here TEMP
## Encryption 
re = Reflector("",list(RESCONFIG["A"]))
r1 = Rotor(1,"A","B","B",list(ROSCONFIG["I"]["Wiring"]))
r2 = Rotor(2,"A","B","B",list(ROSCONFIG["II"]["Wiring"]))
r3 = Rotor(3,"A","B","B",list(ROSCONFIG["III"]["Wiring"]))
pb = PlugBoard()
pb.StandardPlug()

## Main Machine
Machine = Enigma(pb,re,r1,r2,r3,debug)

## Remove all the artifacts
import os
cmd = 'rm -rf *.html'
os.system(cmd)

## RUN
'''
    Example: of Encryption and Decryption
'''
## PlainText
Message = "ciaociao"
CypherT = "LWEUALRN"
print(Machine)
print("Message to be encrypted:     {}".format(Message))
print("Encryption:                  {}".format(Machine.Execute(encryption,Message).upper()))
Machine.ResetEnigma()
print("Decryption:                  {}".format(Machine.Execute(decryption,CypherT).upper()))

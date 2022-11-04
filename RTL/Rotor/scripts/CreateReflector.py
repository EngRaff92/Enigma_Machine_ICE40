'''
    File used as a header to include many Reflector utilities
'''

## Main pakcages
###################
## PATH LOCATOR
###################
from path_locator_lib import *
file    = pcollateral+"./reflector.bin"
cmd     = "rm -rf {}".format(file)

## Main Plugboard
Reflectors = {
    "A"     : "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B"     : "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C"     : "FVPJIAOYEDRZXWGCTKUQSBNMHL",
    "ETW"   : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "UKW"   : "QYHOGNECVPUZTFDJAXWMKISRBL" 
}

## Main Shuffle list routine
def RandList() ->list:
    import random
    t = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.shuffle(t)
    return t

## Main Random Letter setter
def RandChar() ->str:
    import random
    return random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

def ShiftList(n: int, Inlist: list) ->list:
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

## Generate image
def main():
    import os
    import sys
    ## Local Dictionary for Plgging 
    reflector = []
    import argparse
    p   = argparse.ArgumentParser()
    p.add_argument('type', help="constant reflector possible values are: A,B,C,ETW,UKW", type=str)
    p.add_argument('-r', '--random', action='store_true', help="random reflector")
    p.add_argument('-s', '--standard', action='store_true', help="standard plugboard")
    args = p.parse_args()
    if args.type in Reflectors.keys():
        print("Constant Reflector image generation selected")
        # assign the reflector
        reflector = list(Reflectors[args.type])
    else:
        ## Raise a System Error
        print("Constant Reflector image generation selected")
    if args.random:
        print("Random Reflector image generation selected")    
    elif args.standard:
        print("Standard Reflector image generation selected")    
    else:
        ## Raise a System Error
        pass
    
    ## Execute
    if(os.path.exists(file)):
        sys.system(cmd)
    with open(file, 'w') as f:
        for c in reflector:
            ## 6 bits in total
            ## ---- 5 ----- 4 --------- 0
            ##      |       |           |
            ## plugged flag     Plug     
            f.write("0b{:05b}\n".format(convert(c)).replace("0b",""))

if __name__ == "__main__":
    main()
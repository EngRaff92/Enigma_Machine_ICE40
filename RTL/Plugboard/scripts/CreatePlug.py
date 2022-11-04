'''
    File that provides several utilities for PLUGBOARD configuration
'''

## Main pakcages
from PlughBoard_utilis import *
file    = pcollateral+"/plugboard.bin"
cmd     = "rm -rf {}".format(file)

## Main Plugboard
connections = {
    "A":(1,"A"),
    "B":(1,"B"),
    "C":(1,"C"),
    "D":(1,"D"),
    "E":(1,"E"),
    "F":(1,"F"),
    "G":(1,"G"),
    "H":(1,"H"),
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
    ## Local Dictionary for Plgging 
    plugs = {}
    import argparse
    p   = argparse.ArgumentParser()
    p.add_argument('-c', '--constant', action='store_true', help="constant plugboard")
    p.add_argument('-r', '--random', action='store_true', help="random plugboard")
    p.add_argument('-s', '--standard', action='store_true', help="standard plugboard")
    args = p.parse_args()
    if args.constant:
        print("Constant Plugboad image generation selected")    
    elif args.random:
        print("Random Plugboad image generation selected")    
    elif args.standard:
        print("Standard Plugboad image generation selected")    
    else:
        pass
    
    ## TEMP
    plugs = connections
    ## Execute
    if(os.path.exists(file)):
        sys.system(cmd)
    with open(file, 'w') as f:
        for c in plugs.keys():
            ## 6 bits in total
            ## ---- 5 ----- 4 --------- 0
            ##      |       |           |
            ## plugged flag     Plug     
            f.write("1"+"0b{:05b}\n".format(convert(plugs[c][1])+1).replace("0b",""))

if __name__ == "__main__":
    main()
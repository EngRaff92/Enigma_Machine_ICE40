# Enigma on ICE40 (IceSugar)

## Directory Structure

## Python Model

### Enigma 

DO NOT EXPLAIN USING LETTERS but numbers:

Anytime a new letter is pressed it will be converted into a specific number from ASCII based on the convert() function. ONce the corresponding number is given, we determine the entering one by adding the current given letter number with the Start Start which essentially behaves like an offset. So the new KeyLoc (Key Location) will be loc + offset. Since the starting state determines how the Alphabet needs to be shifted. The offset doesn't need to be positive: imagine we are entering C and the initial Mapping should be giving B so the LOC + OFF should be returning B hence we get 2+OFF=1-> OFF=-1.

Generally speaking a new key location is alwasy made by the offset (< or > 0) and the stepping of the rotor, but we cannot overflow the number of element in a rotor or within a give Alphabet hence we neeed to modular add everything to chopp off the final value. The final value needs to be fed into the RING setting. 

The latter will just change how each letter is wired on the output. Meaning if A is wired to M if a move the ring to 2B then A needs ot be mapped to N, this would impact the NOTCH as well. So given the notch the wiring will change the notch. Then the resulting Key in string is already part of the Wiring list we just need to give the index

### Rotors

### Configuration

### Run Tests

### Run Example

### Graph Visualizer 


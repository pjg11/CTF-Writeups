from pwn import *

text = b'[GQh{\'f}g wLqjLg{ Lt{#`g&L#uLpgu&Lc\'&g2n'
print(xor(text, b'\x13'*len(text)))
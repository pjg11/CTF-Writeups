#!/usr/bin/python
# code from: https://github.com/SpiderLabs/cribdrag/blob/master/xorstrings.py

import sys
import argparse

def sxor(s1,s2):    
    # convert strings to a list of character pair tuples
    # go through each tuple, converting them to ASCII code (ord)
    # perform exclusive or on the ASCII code
    # then convert the result back to ASCII (chr)
    # merge the resulting array of characters as a string
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

s1 = "dc0de91face292ed3f3f7337c368b4d02c26cdce7d3537df40497c9b5509063c4aafceb5e3fe".decode('hex')
s2 = "flag{e04f962d0529a4289a685112bfldcdd3}"

s3 = sxor(s1, s2)

# python2 syntax
print s3.encode('hex')
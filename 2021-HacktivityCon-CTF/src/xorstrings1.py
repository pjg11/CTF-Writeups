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

s1 = "ba618878d787a2d959064505a75881e21547f9fc450c56e9787c4daa676b60502eccaad1d083".decode('hex')
s2 = "dc0de91facbe90ee6f652167906ee0d17123cf9e746a63db4b4e7d93040f59331ead9be0b2fe".decode('hex')

s3 = sxor(s1, s2)

# python2 syntax
print s3.encode('hex')
#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

key = hashlib.md5(long_to_bytes(1)).digest()
cipher = AES.new(key, AES.MODE_ECB)
message = cipher.encrypt(b'Initialization Sequence - Code 0')
print(message.hex())
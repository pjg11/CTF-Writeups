#!/usr/bin/env python3
from hashlib import sha256

BLOCK_SIZE = 32

ct = bytes.fromhex("cc088f30119316e5ce4b93d216765ec988ee487fd50a18b9ab42bc44f12268f99a338dc0372c505aa125a948f009cc7bbf6698fa633d0b6049ea5c62857ac3c9702882a1526f2cd658ee1b6d17286f90d471c81dee4d34b02c946277fe75130830a7663fc2558375415e9348dd0f08ebdd07a7f0ead68e84e6581b98e510d70fd6293601c1e38d3cc6abf4ac088201be86ee8e37f448f2de03ce5b24685b84b1bf4f8dc71de075b73456985d01dd7bc012db534cabe443f54593f40b4c4c0482b58d65e15d2b6bf113fb0cad419348ce13d7980e4910014ab97ffa4d6d032c063ff12f7d05513e949edf85f76941904be020784d09c83515dafe4b8740145094")

blocks = [ct[i:i+BLOCK_SIZE] for i in range(0, len(ct), BLOCK_SIZE)]
h = bytes.fromhex("899922c3b025b2c569d32e6fa102f9654ecee51e61eaa55448d057d0c3aef085")
pt = b''

def decrypt_block(block, secret):
	dec_block = b''
	for i in range(BLOCK_SIZE):
		val = (block[i] - secret[i]) % 256

		dec_block += bytes([val])
	return dec_block


for block in blocks:
	dec_block = decrypt_block(block, h)
	h = sha256(block + dec_block).digest()
	pt += dec_block

print("Plaintext: {}".format(pt))
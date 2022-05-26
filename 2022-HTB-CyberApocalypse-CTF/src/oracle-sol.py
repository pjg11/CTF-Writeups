#!/usr/bin/env python3 
import string
from pwn import *

pt = bytes.fromhex("00"*35)

conn = remote('165.227.224.55', 31807)
for c in range(35, 0, -1):
	print(c, "=="*50)
	conn.recvuntil((b'> '))
	conn.sendline("00"*c)
	actual = conn.recvline().decode('utf-8')
	for i in string.printable:
		conn.recvuntil((b'> '))
		send = pt+bytes(i, 'utf-8')
		conn.sendline(bytes.hex(send))
		answer = conn.recvline().decode('utf-8')
		if str(answer[64:96]) == actual[64:96]:
			print("FOUND ", i)
			pt = pt[1:] + bytes(i, 'utf-8')
			print(pt)
			break
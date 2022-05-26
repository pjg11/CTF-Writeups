# The Three Eyed Oracle
### crypto | 300 points | 264 solves

## Description
Feeling very frustrated for getting excited about the AI and not thinking about the possibility of it malfunctioning, you blame the encryption of your brain. Feeling defeated and ashamed to have put Miyuki, who saved you, in danger, you slowly walk back to the lab. More determined than ever to find out what’s wrong with your brain, you start poking at one of its chips. This chip is linked to a decision-making algorithm based on human intuition. It seems to be encrypted… but some errors pop up when certain user data is entered. Is there a way to extract more information and fix the chip?

## First Impressions

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import signal
import subprocess
import socketserver

FLAG = b'HTB{--REDACTED--}'
prefix = random.randbytes(12)
key = random.randbytes(16)


def encrypt(key, msg):
    msg = bytes.fromhex(msg)
    crypto = AES.new(key, AES.MODE_ECB)
    padded = pad(prefix + msg + FLAG, 16)
    return crypto.encrypt(padded).hex()


def challenge(req):
    req.sendall(b'Welcome to Klaus\'s crypto lab.\n' +
                b'It seems like there is a prefix appended to the real firmware\n' +
                b'Can you somehow extract the firmware and fix the chip?\n')
    while True:
        req.sendall(b'> ')
        try:
            msg = req.recv(4096).decode()

            ct = encrypt(key, msg)
        except:
            req.sendall(b'An error occurred! Please try again!')

        req.sendall(ct.encode() + b'\n')


class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(1500)
        req = self.request
        challenge(req)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), incoming)
    server.serve_forever()


if __name__ == "__main__":
    main()

```

We send plaintext, we get ciphertext in return. We can use both to get the flag. However, we only know part of the plaintext, as there is a prefix attached before our message, and the flag is added after our message, as seen from the encrypt function.

```python
def encrypt(key, msg):
    msg = bytes.fromhex(msg)
    crypto = AES.new(key, AES.MODE_ECB)
    padded = pad(prefix + msg + FLAG, 16)
    return crypto.encrypt(padded).hex()
```

AES in ECB mode is known to be a weak cipher as each block is encrypted with the key independently. This mode of operation is prone to the adaptive chosen plaintext attack, which is how we will solve this challenge.

<img src="images/oracle-ecb-dark.png#gh-dark-mode-only" width=100% />
<img src="images/oracle-ecb-light.png#gh-light-mode-only" width=100% />

## Solution

There were two resources that helped me understand this concept:
- [Attacking ECB](https://zachgrace.com/posts/attacking-ecb/) by Zach Grace
- [All-Army CyberStakes! AES-ECB Plaintext Recovery](https://www.youtube.com/watch?v=f-iz_ZAS258) by John Hammond

I'll try my best to summarize the above resources in the context of this solution.

So far, we know from the source code that the encrypted message contains the following parts.

<img src="images/oracle-ct-dark.svg#gh-dark-mode-only" width=100% />
<img src="images/oracle-ct-light.svg#gh-light-mode-only" width=100% />

From the key size and padding amount in the source code, we can infer that the block size is 16 bytes. As the prefix is 12 bytes, we can add 4 more bytes to fill up the first block. As an example, these are the blocks with 20 A's as input - 4 A's to complete the first block and 16 A's to create another block.

<img src="images/oracle-blocks-dark.svg#gh-dark-mode-only" width=100% />
<img src="images/oracle-blocks-light.svg#gh-light-mode-only" width=100% />

from [Attacking ECB](https://zachgrace.com/posts/attacking-ecb/):
> Since each block of plaintext is encrypted with the key independently, identical blocks of plaintext will yield identical blocks of ciphertext. 

So a block with plaintext "AAAAAAAAAAAAAAAA" will produce the same ciphertext everytime. We can use this feature by removing one A from the block. This will make Block 2 19 A's + the first character of the flag, H in this case.

<img src="images/oracle-leak-dark.svg#gh-dark-mode-only" width=100% />
<img src="images/oracle-leak-light.svg#gh-light-mode-only" width=100% />

In the actual scenario, the last byte is unkwown. However, we can brute force the last byte. This would mean creating plaintexts of "AAAAAAAAAAAAAAA_" and compare the resulting ciphertext with the ciphertext above "AAAAAAAAAAAAAAAH" in this example. 

Once the two blocks are equal, we can add the found character to the user input and remove one more A from the block to find the next character. This process repeats till we retrieve the entire flag.

<img src="images/oracle-mleak-dark.svg#gh-dark-mode-only" width=100% />
<img src="images/oracle-mleak-light.svg#gh-light-mode-only" width=100% />

This script implements the above logic with a few changes
- The number of characters being sent are increased to be able to retrieve the entire flag (which is more than 16 bytes in length)
- The hex byte `\x00` is sent in place of A's to avoid any confusion with the letters from the flag.

```python
#!/usr/bin/python3 
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
```

```bash
$ python3 sol.py
...
====================================================================================================
FOUND }
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00HTB{345y_53cr37_r3c0v3ry}'
```

Not very 345y, but surely very satisfying to see the flag being made letter by letter :)

Flag: `HTB{345y_53cr37_r3c0v3ry}`

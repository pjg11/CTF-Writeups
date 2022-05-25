# Jenny From The Block
### crypto | 300 points | 312 solves

## Description
Intrigued by the fact that you have found something your father made, and with much confidence that you can be useful to the team, you rush excitedly to integrate “Jenny” into the spaceship’s main operating system. For weeks, everything went smoothly, until you ran into a meteor storm. Having little to no data of training, the AI is now malfunctioning. Ulysses freaks out because he can no longer control the spaceship due to the AI overriding his manual commands. Big banging noises terrify your crew members. Everything is shaking. It’s time to act. Do you think you can temporarily shut down “Jenny” until she becomes more sophisticated?

## First Impressions

The challenge comes with the following source code:

```python
from hashlib import sha256
from Crypto.Util.Padding import pad, unpad
import signal
import subprocess
import socketserver
import os

allowed_commands = [b'whoami', b'ls', b'cat secret.txt', b'pwd']
BLOCK_SIZE = 32


def encrypt_block(block, secret):
    enc_block = b''
    for i in range(BLOCK_SIZE):
        val = (block[i]+secret[i]) % 256
        enc_block += bytes([val])
    return enc_block


def encrypt(msg, password):
    h = sha256(password).digest()
    if len(msg) % BLOCK_SIZE != 0:
        msg = pad(msg, BLOCK_SIZE)
    blocks = [msg[i:i+BLOCK_SIZE] for i in range(0, len(msg), BLOCK_SIZE)]
    ct = b''
    for block in blocks:
        enc_block = encrypt_block(block, h)
        h = sha256(enc_block + block).digest()
        ct += enc_block

    return ct.hex()


def run_command(cmd):
    if cmd in allowed_commands:
        try:
            resp = subprocess.run(
                cmd.decode().split(' '),  capture_output=True)
            output = resp.stdout
            return output
        except:
            return b'Something went wrong!\n'
    else:
        return b'Invalid command!\n'


def challenge(req):
    req.sendall(b'This is Jenny! I am the heart and soul of this spaceship.\n' +
                b'Welcome to the debug terminal. For security purposes I will encrypt any responses.')
    while True:
        req.sendall(b'\n> ')
        command = req.recv(4096).strip()
        output = run_command(command)
        response = b'Command executed: ' + command + b'\n' + output
        password = os.urandom(32)
        ct = encrypt(response, password)
        req.sendall(ct.encode())


class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(30)
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

The response entered by the user is encrypted by a block cipher, where the password used a random number of length 32. In the encrypt function, we see that each block is encrypted with a different key. However, if we can retrieve the first key, we can retrieve the other keys as well! 

For this attack to work, we would need a plaintext-ciphertext set, at least enough of it to get the key for the first block.


## Solution

The server returned the following response when `cat secret.txt` is entered as input. This gives us the entire ciphertext.

```bash
$ nc 206.189.126.143 31615
This is Jenny! I am the heart and soul of this spaceship.
Welcome to the debug terminal. For security purposes I will encrypt any responses.
> cat secret.txt
cc088f30119316e5ce4b93d216765ec988ee487fd50a18b9ab42bc44f12268f99a338dc0372c505aa125a948f009cc7bbf6698fa633d0b6049ea5c62857ac3c9702882a1526f2cd658ee1b6d17286f90d471c81dee4d34b02c946277fe75130830a7663fc2558375415e9348dd0f08ebdd07a7f0ead68e84e6581b98e510d70fd6293601c1e38d3cc6abf4ac088201be86ee8e37f448f2de03ce5b24685b84b1bf4f8dc71de075b73456985d01dd7bc012db534cabe443f54593f40b4c4c0482b58d65e15d2b6bf113fb0cad419348ce13d7980e4910014ab97ffa4d6d032c063ff12f7d05513e949edf85f76941904be020784d09c83515dafe4b8740145094
```

```python
response = b'Command executed: ' + command + b'\n' + output
```

This line from the source code gives us an insight into the plaintext. So far, the words `Command executed: cat secret.txt\n` are known, which also happens to be the size of one block! We can use 32 bytes of the ciphertext and the known plaintext to find out the key as follows

```python
BLOCK_SIZE = 32

pt = b'Command executed: cat secret.txt\n'
ct = bytes.fromhex("cc088f30119316e5ce4b93d216765ec988ee487fd50a18b9ab42bc44f12268f99a338dc0372c505aa125a948f009cc7bbf6698fa633d0b6049ea5c62857ac3c9702882a1526f2cd658ee1b6d17286f90d471c81dee4d34b02c946277fe75130830a7663fc2558375415e9348dd0f08ebdd07a7f0ead68e84e6581b98e510d70fd6293601c1e38d3cc6abf4ac088201be86ee8e37f448f2de03ce5b24685b84b1bf4f8dc71de075b73456985d01dd7bc012db534cabe443f54593f40b4c4c0482b58d65e15d2b6bf113fb0cad419348ce13d7980e4910014ab97ffa4d6d032c063ff12f7d05513e949edf85f76941904be020784d09c83515dafe4b8740145094")

blocks = [ct[i:i+BLOCK_SIZE] for i in range(0, len(ct), BLOCK_SIZE)]
key = b''

for j in range(BLOCK_SIZE):
	for i in range(256):
		val = (pt[j]+i) % 256
		if val == blocks[0][j]:
			key += bytes([i])
			break

print("Key: {}".format(key.hex()))
```

```bash
$ python3 findkey.py
Key: 899922c3b025b2c569d32e6fa102f9654ecee51e61eaa55448d057d0c3aef085
```

With one key, we can calculate the other keys exactly like in the source code. The following script calculates the keys and decrypts the encrypted text.

```python
from hashlib import sha256
from Crypto.Util.Padding import pad, unpad
import signal
import subprocess
import socketserver
import os

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
```

```bash
$ python3 sol.py
Plaintext: b'Command executed: cat secret.txt\nIn case Jenny malfunctions say the following phrase: Melt My Eyez, See Your Future  \nThe AI system will shutdown and you will gain complete control of the spaceship.\n- Danbeer S.A.\nHTB{b451c_b10ck_c1ph3r_15_w34k!!!}\n\x07\x07\x07\x07\x07\x07\x07'
```

Flag: `HTB{b451c_b10ck_c1ph3r_15_w34k!!!}`

# Android-in-the-Middle
### crypto | 300 points | 505 solves

## Description
Years have passed since Miyuki rescued you from the graveyard. When Virgil tells you that he needs your help with something he found there, desperate thoughts about your father and the disabilities you developed due to the disposal process come to mind. The device looks like an advanced GPS with AI capabilities. Riddled with questions about the past, you are pessimistic that you could be of any value. After hours of fiddling and observing the power traces of this strange device, you and Virgil manage to connect to the debugging interface and write an interpreter to control the signals. The protocol looks familiar to you. Your father always talked about implementing this scheme in devices for security reasons. Could it have been him?

## First Impressions

There is a server the user can connect to, and the code running on the server is provided as a challenge file, `source.py`

```python
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib
import random
import socketserver
import signal


FLAG = "HTB{--REDACTED--}"
DEBUG_MSG = "DEBUG MSG - "
p = 0x509efab16c5e2772fa00fc180766b6e62c09bdbd65637793c70b6094f6a7bb8189172685d2bddf87564fe2a6bc596ce28867fd7bbc300fd241b8e3348df6a0b076a0b438824517e0a87c38946fa69511f4201505fca11bc08f257e7a4bb009b4f16b34b3c15ec63c55a9dac306f4daa6f4e8b31ae700eba47766d0d907e2b9633a957f19398151111a879563cbe719ddb4a4078dd4ba42ebbf15203d75a4ed3dcd126cb86937222d2ee8bddc973df44435f3f9335f062b7b68c3da300e88bf1013847af1203402a3147b6f7ddab422d29d56fc7dcb8ad7297b04ccc52f7bc5fdd90bf9e36d01902e0e16aa4c387294c1605c6859b40dad12ae28fdfd3250a2e9
g = 2


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(0)
        main(self.request)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def sendMessage(s, msg):
    s.send(msg.encode())


def recieveMessage(s, msg):
    sendMessage(s, msg)
    return s.recv(4096).decode().strip()


def decrypt(encrypted, shared_secret):
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.decrypt(encrypted)
    return message


def main(s):
    sendMessage(s, DEBUG_MSG + "Generating The Global DH Parameters\n")
    sendMessage(s, DEBUG_MSG + f"g = {g}, p = {p}\n")
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n\n")

    sendMessage(s, DEBUG_MSG + "Generating The Public Key of CPU...\n")
    c = random.randrange(2, p - 1)
    C = pow(g, c, p)
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n")
    sendMessage(s, DEBUG_MSG + "Public Key is: ???\n\n")

    M = recieveMessage(s, "Enter The Public Key of The Memory: ")

    try:
        M = int(M)
    except:
        sendMessage(s, DEBUG_MSG + "Unexpected Error Occured\n")
        exit()

    sendMessage(s, "\n" + DEBUG_MSG + "The CPU Calculates The Shared Secret\n")
    shared_secret = pow(M, c, p)
    sendMessage(s, DEBUG_MSG + "Calculation Complete\n\n")

    encrypted_sequence = recieveMessage(
        s, "Enter The Encrypted Initialization Sequence: ")

    try:
        encrypted_sequence = bytes.fromhex(encrypted_sequence)
        assert len(encrypted_sequence) % 16 == 0
    except:
        sendMessage(s, DEBUG_MSG + "Unexpected Error Occured\n")
        exit()

    sequence = decrypt(encrypted_sequence, shared_secret)

    if sequence == b"Initialization Sequence - Code 0":
        sendMessage(s, "\n" + DEBUG_MSG +
                    "Reseting The Protocol With The New Shared Key\n")
        sendMessage(s, DEBUG_MSG + f"{FLAG}")
    else:
        exit()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), Handler)
    server.serve_forever()
```
Some lines of code provide more insight into how to get the flag.

```python
sendMessage(s, DEBUG_MSG + "Generating The Global DH Parameters\n")
```

Since this is a crypto challenge, DH in this case probably stands for Diffie Hellman, a protocol to exchange secret keys. One of the attacks on Diffie Hellman is the Man-in-the-Middle attack, which is similar to the name of this challenge. I've never tried MitM attacks before this, so this was cool to try out.

```python
sendMessage(s, DEBUG_MSG + "Public Key is: ???\n\n")
```

Oh. Generally in MitM attacks, the public key is known to both parties. Since we don't know what the public key is here, there has to be another way to get the flag.

```python
shared_secret = pow(M, c, p)
```

`M` is our public key. In Diffie-Hellman, the shared secret is calculated with the public keys of both users.

```python
encrypted_sequence = recieveMessage(s, "Enter The Encrypted Initialization Sequence: ")
if sequence == b"Initialization Sequence - Code 0":
        sendMessage(s, "\n" + DEBUG_MSG +
                    "Reseting The Protocol With The New Shared Key\n")
        sendMessage(s, DEBUG_MSG + f"{FLAG}")
```

The message we send has to be encrypted using the shared secret, so we need to know what the shared secret is to be able to do so. We also know that the sequence `Initialization Sequence - Code 0` needs to be encrypted correctly to get the flag.

```python
def decrypt(encrypted, shared_secret):
    key = hashlib.md5(long_to_bytes(shared_secret)).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    message = cipher.decrypt(encrypted)
    return message
```

The encryption used here is AES, in ECB mode. Since AES is a symmetric cipher, the encryption method will be almost the same as the above method.

## Solution

While searching for possible attacks, I saw a challenge where the public key we send is 1. In that case, the shared secret will be calculated as 1 irrespective of the other user's public key.

With that in mind, I encrypted the sequence with the key 1.

```python
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
import hashlib

key = hashlib.md5(long_to_bytes(1)).digest()
cipher = AES.new(key, AES.MODE_ECB)
message = cipher.encrypt(b'Initialization Sequence - Code 0')
print(message.hex())
```

```bash
$ python3 encrypt.py 
7fd4794e77290bf65808e95467f284966d71995c16e83da2192aecfd2d0df7a4
```

I then connected to the challenge server, entered the public key and encrypted message and got the flag!

```bash
$ nc 134.209.22.191 32230
DEBUG MSG - Generating The Global DH Parameters
DEBUG MSG - g = 2, P = 10177459997049772558637057109490700048394574760284564283959324525695097805837401714582821820424475480057537817583807249627119267268524840254542683041588432363128111683358536204391767254517057859973149680238170237977230020947732558089671785239121778309357814575486749623687357688511361367822815452806637006568922401890961240475060822815400430220536180181951862931844638638933951683988349468373510128406899660648258602475728913837826845743111489145006566908004165703542907243208106044538037004824530893555918497937074663828069774495573109072469750423175863678445547058247156187317168731446722852098571735569138516533993
DEBUG MSG - Calculation Complete

DEBUG MSG - Generating The Public Key of CPU
DEBUG MSG - Calculation Complete
DEBUG MSG - Public Key is: ???

Enter The Public Key of The Memory: 1

DEBUG MSG - The CPU Calculates The Shared Secret
DEBUG MSG - Calculation Complete

Enter The Encrypted Initialization Sequence: 7fd4794e77290bf658sto0895467f284966d71995c1683da2192aecfd2d0df7a4

DEBUG MSG - Resting The Protocol With The New Shared Key
DEBUG MSG - HTB{7h15_p2070c01_15_pr0tec73d_8y_D@nb3er_cOpyr1gh7_1aws}
```

Flag: `HTB{7h15_p2070c01_15_pr0tec73d_8y_D@nb3er_cOpyr1gh7_1aws}`

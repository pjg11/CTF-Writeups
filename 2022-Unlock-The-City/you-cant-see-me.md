# You Can't See Me
easy | network, ics | 100 points

## Description
We have collected information from a small ICS network. Can you uncover all the data hidden in these files? 

## First Impressions

## Solution

### [30 points] Parts make a Whole
The file shows communication between a PLC and an ICS workstation. Analyze the file to get the flag! (use modbus.pcapng)

### [20 points] whoami
There seems to be some suspicious activity in the network. Can you identify the IP address of the rogue ICS component? (use network.pcapng)

### [20 points] man-in-the-middle
What is the protocol used in the Man-in-the-Middle attack performed by the rogue ICS component in this network? (use network.pcapng), Flag format CTF{protocol_in_capital_letters}

### [30 points] Follow me till the End
The rogue component is communicating with an external entity, which is a big red flag in ICS environments. Can you find the flag from the network data?(use network.pcapng)
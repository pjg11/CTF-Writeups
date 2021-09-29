![](images/8-header.png)

# N1TP
### easy | cryptography | 50 points
<br/>

## Challenge Information
These warmups are just too easy! This one definitely starts that way, at least!
<br/><br />

- shows file encrypted with a one time pad with the length same as the flag
- gives you the option to encrypt other texts with the **same one time pad**
- realized this much later, but this is a known plaintext attack, where you can XOR the flag and the plaintext to reveal the key.
- I found a script from another similar challenge writeup called xorstrings.py
- modified it to include the flag and the plaintext, ran it, got key
- modified the script again to include key and cipher text, and got the flag!
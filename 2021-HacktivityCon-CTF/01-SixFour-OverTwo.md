# Six Four Over Two
easy | warmups | 50 points

>I wanted to cover all the bases so I asked my friends what they thought, but they said this challenge was too basic...

The challenge included a text file with the following text

```
EBTGYYLHPNQTINLEGRSTOMDCMZRTIMBXGY2DKMJYGVSGIOJRGE2GMOLDGBSWM7IK
```

After getting confused multiple times on what "Six Four Over Two" actually meant, I finally came to the conclusion that the above text was encoded in base32.

```
$ echo EBTGYYLHPNQTINLEGRSTOMDCMZRTIMBXGY2DKMJYGVSGIOJRGE2GMOLDGBSWM7IK | base32 -d
flag{a45d4e70bfc407645185dd9114f9c0ef}
```

Flag: `flag{a45d4e70bfc407645185dd9114f9c0ef}`
# Space Snacks
beginner | misc | 200 points

## [20 points] Roten to the core
>You find a roten apple next to a piece of paper with 13 circles on and some text. What's the message?
>```
>Vg nccrnef lbh unq jung vg gnxrf gb fbyir gur svefg pyhr  
>Jryy Qbar fcnpr pnqrg  
>pgs{Lbh_sbhaq_gur_ebg}  
>Npprff pbqr cneg 1: QO
>```

**Solution:** Good ol' ROT13 :)

```
It appears you had what it takes to solve the first clue
Well Done space cadet
ctf{You_found_the_rot}
Access code part 1: DB
```
Flag: `ctf{You_found_the_rot}`

## [25 points] The roman space empire
>You find a page with a roman insignia at the top with some text what could it mean?  
>```
>Jhlzhy ulcly dhz clyf nvvk ha opkpun tlzzhnlz.  
>jam{Aol_vul_aybl_zhshk}  
>jvkl whya: NW
>```

**Solution:** Caesar cipher with shift 7.

```
Caesar never was very good at hiding messages.  
ctf{The_one_true_salad}  
code part: GP
```

Flag: `ctf{The_one_true_salad}`

## [25 points] The space station that rocked
>You hear the heavy base line of 64 speakers from the next compartment. you walk in and the song changes to writing's on the wall, there is some strange code painted on the wall what could it mean?
>
>```
>RXZlbiAgaW4gc3BhY2Ugd2UgbGlrZSB0aGUgYnV0dGVyeSBiaXNjdXQgYmFzZS4gY3Rme0lfbGlrZV90aGVfYnV0dGVyeV9iaXNjdWl0X2Jhc2V9IC4gQWNjZXNzIHBhcnQgMzogWEQ=
>```

**Solution:** base64 decoding to the rescue!

```
Even  in space we like the buttery biscut base. 
ctf{I_like_the_buttery_biscuit_base} . Access part 3: XD
```

Flag: `ctf{I_like_the_buttery_biscuit_base}`

## [25 points] What the beep is that?
>You hear beeps on the radio, maybe someone is trying to communicate? Flag format: CTF:XXXXXX
>```
>.. -. ... .--. . -.-. - --- .-. / -- --- .-. ... . / .-- --- ..- .-.. -.. / -... . / .--. .-. --- ..- -.. / --- ..-. / -.-- --- ..- .-. / . ..-. ..-. --- .-. - ... .-.-.- / -.-. - ..-. ---... ... .--. .- -.-. . -.. .- ... .... ..--- ----- ..--- .---- / .- -.-. -.-. . ... ... / -.-. --- -.. . ---... / .--- --...
>```

**Solution:** morse code

```
INSPECTOR MORSE WOULD BE PROUD OF YOUR EFFORTS. CTF:SPACEDASH2021 ACCESS CODE: J7
```

Flag: `CTF:SPACEDASH2021`

## [25 points] The container docker
>You are now in the space cafe, the cake is in the container that should not be here. You can see random names on all the containers. What will Docker never name a container? Note: Please enter it as ctf{full_name}

**Solution:** A [quick search](https://medium.com/peptr/why-boring-wozniak-will-never-be-generated-as-a-container-name-in-docker-763b755f9e2a) reveals `boring-wozniak` as the answer. From Docker's source code:

```go
if name == "boring_wozniak" /* Steve Wozniak is not boring */ {
    goto begin
}
```

Flag: `ctf{boring_wozniak}`

## [50 points] There might be more cake
>They ate then cake and left a note with a secret algorithm to unlock the cake treasury. We saw it happening at exactly January 1, 2030 11:23:45 AM... are you the visionary that can figure out the PIN code? PIN code generation algorithm:
>```
>int generatePin() {
>srand(time(0));
>return rand();
>}
>```

**Solution:** The time mentioned in the description is the seed. `srand()` takes time in the Unix timestamp, which is the number of seconds since January 1, 1970. We can convert the provided timestamp using an [online converter](https://www.epochconverter.com) with the timezone set to GMT. The resulting timestamp is `1893497025`.

This number can be used to complete the provided generation algorithm.

```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int generatePin() {
    
    srand(1893497025);
    return rand();
}

int main()
{
    printf("%d\n", generatePin());
    return 0;
}
```

Running this gives us the PIN code, which is the flag for this challenge.

```
$ gcc -o pin pin.c
$ ./pin
1376299761
```

The program, [pin.c](src/pin.c), works perfectly on Linux, however returns incorrect output on Mac, possibly due to different implementations of `gcc`.

Flag: `1376299761`

## [30 points] Stars in space
>The treasury consists of cake hidden on stars in space.
>```
>* ****  * * * *** ***  **    *  *  * ****  * ** >*  ** ***  ** ***  ** * *  *   ** *     *  * ** >*  *   ** *     *   **  *   *****  **** *  ***  >*  ** * *     * 
>```

**Solution:** Replace the stars with 0s and the spaces with 1s. 

```
0100001101010100010001100111101101101000011010010110010001100100011001010110111001011111011010010110111001011111011100110111000001100001011000110110010101111101
```

Converting the binary to text reveals the challenge flag.

Flag: `CTF{hidden_in_space}`
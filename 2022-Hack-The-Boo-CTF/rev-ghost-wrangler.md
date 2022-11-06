# Ghost Wrangler
easy | rev | 200pts

>Who you gonna call?

## First Impressions

```
$ ./ghost
|                                       _| I've managed to trap the flag ghost in this box, but it's turned invisible!
Can you figure out how to reveal them?
```

Opening the binary in a reverse engineering tool shows the invisible text.

```c
int32_t main(int32_t argc, char** argv, char** envp)

{
    printf(&*"[[GQh{\'f}g wLqjLg{ Lt{#`g&L#uLpgu&Lc\'&g2n%s\r" [0x28], get_flag(), 0x28, 0x5f);
    return 0;
}
```

It calls a get_flag() function, which performs an XOR on the individual bytes with the hex value 0x13.

```c
void* get_flag()

{
    void* rax = malloc(0x29);
    memset(rax, 0, 0x29);
    for (int32_t var_c = 0; var_c <= 0x27; var_c = (var_c + 1))
    {
        *(int8_t*)((char*)rax + ((int64_t)var_c)) = (*"[GQh{'f}g wLqjLg{ Lt{#`g&L#uLpgu…"[((int64_t)var_c)] ^ 0x13);
    }
    return rax;
}
```

## Solution

The text can be XORed with `0x13` to reveal the flag, with the help of a quick python script

**[ghost-sol.py](src/ghost-sol.py)**
```python
from pwn import *

text = b'[GQh{\'f}g wLqjLg{ Lt{#`g&L#uLpgu&Lc\'&g2n'
print(xor(text, b'\x13'*len(text)))
```

```txt
$ python3 ghost-sol.py
b'HTB{h4unt3d_by_th3_gh0st5_0f_ctf5_p45t!}'
```

Flag: `HTB{h4unt3d_by_th3_gh0st5_0f_ctf5_p45t!}`



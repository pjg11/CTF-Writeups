# Ouija
easy | rev | 200pts

>You've made contact with a spirit from beyond the grave! Unfortunately, they speak in an ancient tongue of flags, so you can't understand a word. You've enlisted a medium who can translate it, but they like to take their time...

## First Impressions

```txt
$ ./ouija
Retrieving key.
.....
```
There is no flag in the output, instead dots are printed after every few seconds. There might be more to the program, however I stopped it pretty early on and moved on to viewing the source code.

Opening the binary in a reverse engineering tool reveals the text in the main function. There are a lot of sleep() commands, which meant the program would go on for much longer.

```c
int32_t main(int32_t argc, char** argv, char** envp)
{
    setvbuf(fp: stdout, buf: nullptr, mode: 2, size: 0)
    char* rax = strdup(s: "ZLT{Svvafy_kdwwhk_lg_qgmj_ugvw_escwk_al_wskq_lg_ghlaearw_dslwj!}")
    puts(str: "Retrieving key.")
    sleep(seconds: 0xa)
...
}
```

## Solution

The text looks like something that could be the result of a [Caesar cipher operation](https://www.dcode.fr/caesar-cipher). And it indeed was, as a shift of 8 revealed the flag.

Flag: `HTB{Adding_sleeps_to_your_code_makes_it_easy_to_optimize_later!}`
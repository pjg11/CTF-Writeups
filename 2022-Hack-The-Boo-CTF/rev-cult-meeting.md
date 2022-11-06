# Cult Meeting
easy | rev | 200pts

>After months of research, you're ready to attempt to infiltrate the meeting of a shadowy cult. Unfortunately, it looks like they've changed their password!

## First Impressions

```txt
$ nc 159.65.48.79 32729
You knock on the door and a panel slides back
|/👁️ 👁️ \| A hooded figure looks out at you
"What is the password for this week's meeting?"
```

A password is required to complete the challenge. 

## Solution

Opening the binary in a reverse engineering tool shows the password, `sup3r_s3cr3t_p455w0rd_f0r_u!` in the main function.

```c
int32_t main(int32_t argc, char** argv, char** envp)

{
    setvbuf(stdout, nullptr, 2, 0);
    puts("\x1b[3mYou knock on the door and…");
    puts(&data_2040);
    fwrite("What is the password for this w…", 1, 0x30, stdout);
    void var_48;
    fgets(&var_48, 0x40, stdin);
    *(int8_t*)strchr(&var_48, 0xa) = 0;
    if (strcmp(&var_48, "sup3r_s3cr3t_p455w0rd_f0r_u!") != 0)
    ...
```

After entering the password, a shell appears, with the current directory containing the flag.

```txt
...
"What is the password for this week's meeting?" sup3r_s3cr3t_p455w0rd_f0r_u!
sup3r_s3cr3t_p455w0rd_f0r_u!
The panel slides closed and the lock clicks
|      | "Welcome inside..."
/bin/sh: 0: can't access tty; job control turned off
$ ls
ls
flag.txt  meeting
$ cat flag.txt
cat flag.txt
HTB{1nf1ltr4t1ng_4_cul7_0f_str1ng5}
```

Flag: `HTB{1nf1ltr4t1ng_4_cul7_0f_str1ng5}`





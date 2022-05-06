# Prisoner
### easy | Warmups | 50 points

## Description
Have you ever broken out of jail? Maybe it is easier than you think! 
<br /><br />

## Solution
The challenge provides an ssh server to log into:
```bash
ssh challenge@nahamcon.com 22322
# password is 'userpass'
```

Once logged in, it shows the following screen

![](images/prisoner-ssh.png)

No matter what I type here, nothing happens.

Suddenly, I had the idea to press Ctrl+D. And I see the following message:
```bash
: Traceback (most recent call last):
  File "/home/user/jail.py", line 27, in <module>
      input(": ")
EOFError
>>>
```

OH, so that was a python program running that we exited from? Yup, turns out there is a thing called "Python sandbox escaping", explained in this line from [this link](https://github.com/mahaloz/ctf-wiki-en/blob/master/docs/pwn/linux/sandbox/python-sandbox-escape.md):
>What we usually call Python sandbox escaping is to bypass the simulated Python terminal and ultimately implement command execution.

Cool! So now we have access to the system's files, and we need to find the flag. One of the python functions is `os.system()` that let's a user run system commands.

![](images/prisoner-flag.png)

First, `import os` to be able to use the system() command. Then I checked the current directory using `os.system('ls')` and found the flag in the same directory! Then we can retrieve the flag using `os.system('cat flag.txt')`. Challenge complete!

Flag: `flag{c31e05a24493a202fad0d1a827103642}`
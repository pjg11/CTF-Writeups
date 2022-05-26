# WIDE
### rev | 300 points | 1473 solves

## Description
We've received reports that Draeger has stashed a huge arsenal in the pocket dimension Flaggle Alpha. You've managed to smuggle a discarded access terminal to the Widely Inflated Dimension Editor from his headquarters, but the entry for the dimension has been encrypted. Can you make it inside and take control?

## First Impressions

We're provided with a binary name `wide` and what seems to be a database file, called `db.ex`. On running the binary as is, the following error shows up

```bash
$ ./wide
Usage: ./wide db.ex
```
With the correct usage, the output displays a set of names and codes

```bash
$ ./wide db.ex
[*] Welcome user: kr4eq4L2$12xb, to the Widely Inflated Dimension Editor [*]
[*]    Serving your pocket dimension storage needs since 14,012.5 B      [*]
[*]                       Displaying Dimensions....                      [*]
[*]       Name       |              Code                |   Encrypted    [*]
[X] Primus           | people breathe variety practice  |                [*]
[X] Cheagaz          | scene control river importance   |                [*]
[X] Byenoovia        | fighting cast it parallel        |                [*]
[X] Cloteprea        | facing motor unusual heavy       |                [*]
[X] Maraqa           | stomach motion sale valuable     |                [*]
[X] Aidor            | feathers stream sides gate       |                [*]
[X] Flaggle Alpha    | admin secret power hidden        |       *        [*]
Which dimension would you like to examine? 6
[X] That entry is encrypted - please enter your WIDE decryption key: 
```

`Flaggle Alpha` sounds close to "flag", and it's the only one encrypted which means that this is where the flag is stored. We need to find the decryption key from the binary provided

## Solution

I viewed the binary in Binary Ninja, a reverse engineering tool. Starting from the main function of the program, I found the decryption key, `sup3rs3cr3tw1d3` in the menu() function.

![](images/rev-secret.png)

Entering this key when running the program retrieves the flag.

```bash
...
Which dimension would you like to examine? 6
[X] That entry is encrypted - please enter your WIDE decryption key: sup3rs3cr3tw1d3
HTB{str1ngs_4r3nt_4lw4ys_4sc11}
Which dimension would you like to examine?
```

Flag: `HTB{str1ngs_4r3nt_4lw4ys_4sc11}`

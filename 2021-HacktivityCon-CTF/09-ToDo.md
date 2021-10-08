![](images/9-header.png)

# To Do
### easy | mobile | 50 points  
<br/>

## Challenge Information
I made my own app to remind me of all the things I need to do
<br/><br />

## Solution
What I thought would be the hardest easy challenge, turned out to be the challenge I solved the fastest!

The challenge included an `.apk` file. Knowing nothing about mobile CTF challenges, I started looking through the files and folders in this apk file.

![](images/9-files.png)

I ended up finding a file called `todos.db` in `/assets/databases`

![](images/9-db.png)

Again, not knowing what exactly to search for, I started browsing through the different options, and found some data in the `Browse Data` section

![](images/9-flag.png)

The `=` at the end confirmed that this was base64 encoded data. The first few letters reminded me of the text from the [Bass64 challenge](4-Bass64.md), which meant that decoding this would output the flag for the challenge!

![](images/9-decode.png)

Flag: `flag{526eab04ff9aab9ea138903786a9878b}`
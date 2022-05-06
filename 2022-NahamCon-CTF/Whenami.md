# WhenAmI
### easy | Miscellaneous | 284 points

## Description
I know where I am, but... when am I? 

NOTE: Flag submission format is flag{[number of seconds goes here]}, such as flag{600}.

## Solution

The challenge came with a file, `challenge.txt`

```txt
When am I??

So, I look down at my watch. It's December 28, 2011 at 11:59AM, and I'm just minding my own business at -13.582075733990298, -172.5084838587106.
I hung out there until the local time was 1:00AM on December 31st, and then I hopped on a plane and took a 1 hour flight over to -14.327595989244111, -170.71287979386747.
Some time has passed since I landed, and on December 30th, 12PM local time, I took a 1 hour flight back to my original location.
It's been 10 hours since I landed on my most recent flight - how many seconds have passed since I first looked at my watch?

(Submission format is flag{<number of seconds goes here>}, such as flag{600}.)

```

There are a lot of dates and times, and just a lot of numbers in general. Let's start bit by bit.

First up, the coordinates.
-13.582075733990298, -172.5084838587106: A'opo Conservation Area, Samoa (GMT +13)
-14.327595989244111, -170.71287979386747: Tualauta, Western District, American Samoa (GMT -11)
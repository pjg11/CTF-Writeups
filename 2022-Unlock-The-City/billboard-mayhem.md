# Billboard Mayhem
easy | web | 100 points

## Description
The AI is showing off its neural network all over the city by taking over the billboards. Can you take back control and discover what the AI left behind? 

## First Impressions

The website displays a billboard containing an image. 

![](images/bm-website.png)


## Solution

### [10 points] Find the upload form
The AI has hidden our upload form. Can you find the upload form?

In an attempt to check the source code, I hovered the mouse over the billboard, and saw the flag!

![](images/bm-1-flag.png)

Flag: `CTF{e8a63b628756eb0023899b3a7f60825c}`

### [90 points] Billboard Control
Our development team has picked up that the AI has included their own secret code to our environment variables. Can you upload a new advertisement that displays these values? (Always remember to be smarty with your payload!)

The other side of the billboard contains a link to upload an advertisement. What we upload will then be displayed in place of the image. The advertisement has to be in TPL format, which is a format I hadn't heard of before. After a quick search, I found out that its a PHP template file, in which one can place variables that can be parsed different depending on the content of the variable[^1]. This website also had a sample TPL file, so I used the same and tweaked it a bit for this challenge.

**[advertisement.tpl](src/bm-2-advertisement.tpl)**
```tpl
<html>
    <head>
        <title>Info</title>
    </head>
    <body>
      <pre>
       {$flag}
      </pre>
    </body>
</html>
```

On uploading the file, the billboard now displayed the flag for the challenge!

![](images/bm-2-flag.png)

Flag: `CTF{c72edca19622b230bdfb4bfae250dbc8}`


[^1]: From https://www.geeksforgeeks.org/what-is-tpl-file-in-php-web-design/
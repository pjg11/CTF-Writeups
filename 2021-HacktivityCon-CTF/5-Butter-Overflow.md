![](images/5-header.png)

# Butter Overflow
### easy | warmups | 50 points  
<br/>

## Challenge Information
Can you overflow this right?
<br/><br />

- a very simple buffer overflow challenge that I still took forever to complete
- there are three files, a makefile, the source code and the resulting executable
- the source code shows the buffer is 200 chars long, and the flag is printed when a segmentation fault takes place.
- tried passing it by setting a number higher than 200, didn't work
- then looked stuff up bcoz genuinely confused
- then sent a much higher number (1200), seg fault happened, flag received!
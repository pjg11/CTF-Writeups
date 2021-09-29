![](images/8-header.png)
# Cute Invoice
### medium | crypto | 200 points
<br/>

## Challenge Information
Who knew invoices could be cute?
<br/><br />

## Sub-Challenges
### [200 points] Cute Invoice
Who knew invoices could be secure AND cute? Our third-party contractor for space shuttle parts is using the best tooling for sending us secure invoices.
### Solution 
There were two files attached with the challenge, invoice.pdf and invoice.png.

![](images/invoicepdf.png)

On opening invoice.pdf, we see that it is password protected. Tools like qpdf can be used to unlock the password, however we do require a list of passwords to check against the pdf.

![](images/invoice.png)

The following details from the image serve as clues to solving the challenge:
- The password generator used is QtPass v1.2.0, which will be referenced shortly.
- The password is 16 characters long
- The character set used is 'All Characters'

The initial idea was to brute force the password, which was not the correct approach for this challenge. I even went to the extent of cracking the password using an incremental mode in John the Ripper, setting a length of 16 chars and setting the mode to alphanumeric. I quickly realized that this was not the right way, as it that way would have taken forever. There had to be some catch to this.

Then my attention went towards the name and version of the password manager itself. A search for this version on Google revealed a flaw in the way the password is generated.
##### from https://github.com/IJHack/QtPass/issues/338
![](images/thevuln.png)

The seed provided to the random number generator is the milliseconds past since the last second. Due to this, there are only 1000 possible seeds, hence only 1000 possible passwords!

So if I were able to write an application to run the password generating function provided in the above link and generate the 1000 passwords, then cracking the password should be pretty easy!

### Generating the Passwords

### 1. Get information on the character set used
The password generating function takes characters from a charset. On searching the source code of this application on GitHub (specifically v1.2.0), the characters in each charset were found in [datahelpers.h](https://github.com/IJHack/QtPass/blob/v1.2.0/src/datahelpers.h)

### 2. Install Qt 
It is preferred to use the Online Installer as it makes the installation process a lot smoother than the offline installers. I initially installed the most recent version of Qt, which is 6.1.2, however as I began writing the application, I found that some functions were made obsolete in this version. So I installed Qt 5.1.5 later on. However it is possible to install it from the Online Installer directly.

![](images/qtinstall.gif)

Installing Qt will also install Qt Creator, the IDE used to create Qt applications. On opening Qt Creator, click on New > Qt Console Application. Follow the setup instructions and the application should be created.

### 3. Writing the application

#### [8-password-cracker.cpp](https://github.com/piyagehi/CTF-Writeups/blob/main/2021-Space-Race/src/cute-invoice.cpp).
```c++
#include <QtCore/QCoreApplication>
#include <QtCore/qglobal.h>
#include <QtGlobal>
#include <QString>
#include <iostream>


int main()
{
    QString charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~!@#$%^&*()_-+={}[]|:;<>,.?";
    int length = 16;

    for (int i = 0; i < 1000; i++)
    {
        qsrand(i);
        QString passwd = NULL;
        for (int j = 0; j < length; ++j)
        {
            int index = qrand() % charset.length();
            QChar nextChar = charset.at(index);
            passwd.append(nextChar);
        }
        qDebug("%s", qUtf8Printable(passwd));
    }
    return 0;
}
```

Running this code returns 1000 passwords in the output, which are then copied in a text file.

<p align=center><img src="images/passwords.png" height=50% width=50%></p>

A bash script runs qpdf to check each password against the pdf file and prints the password when found.

#### [8-script.sh](https://github.com/piyagehi/CTF-Writeups/blob/main/2021-Space-Race/src/8-script.sh)

```bash
#!/bin/bash
filename="passwords.txt"
while read password;
do
        qpdf --password=$password --decrypt invoice.pdf invoiceout.pdf 2>/dev/null 
        if [ -f invoiceout.pdf ]
        then
                echo "Password found:" $password
                break
        fi
done < $filename
```

The password is found, and the unlocked pdf is saved as invoiceout.pdf. 
```shell
piyagehi@Piyas-MacBook-Pro:~$ ./script.sh
Password found: M=ZjV1z40MQF. 5HM
```

The flag is revealed in invoiceout.pdf
![](images/invoiceout.png)

Flag: `CTF{b256d0dae143bb6fd688b4cdd4fbc7d2}`
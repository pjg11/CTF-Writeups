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
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
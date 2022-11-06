# Fast Carmichael
easy | crypto | 200pts

>You are walking with your friends in search of sweets and discover a mansion in the distance. All your friends are too scared to approach the building, so you go on alone. As you walk down the street, you see expensive cars and math papers all over the yard. Finally, you reach the door. The doorbell says "Michael Fastcar". You recognize the name immediately because it was on the news the day before. Apparently, Fastcar is a famous math professor who wants to get everything done as quickly as possible. He has even developed his own method to quickly check if a number is a prime. The only way to get candy from him is to pass his challenge.

## First Impressions

The challenge comes with a script, `server.py`

```python
from Crypto.Util.number import isPrime
import socketserver
import signal


FLAG = "HTB{}"

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        signal.alarm(0)
        main(self.request)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def sendMessage(s, msg):
    s.send(msg.encode())


def receiveMessage(s, msg):
    sendMessage(s, msg)
    return s.recv(4096).decode().strip()


def generate_basis(n):
    basis = [True] * n

    for i in range(3, int(n**0.5) + 1, 2):
        if basis[i]:
            basis[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)

    return [2] + [i for i in range(3, n, 2) if basis[i]]


def millerRabin(n, b):
    basis = generate_basis(300)
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _isPrime(p):
    if p < 1:
        return False
    if not millerRabin(p, 300):
        return False

    return True


def main(s):
    p = receiveMessage(s, "Give p: ")

    try:
        p = int(p)
    except:
        sendMessage(s, "Error!")
        print("here")
    if _isPrime(p) and not isPrime(p):
        sendMessage(s, FLAG)
    else:
        sendMessage(s, "Conditions not satisfied!")


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), Handler)
    server.serve_forever()
```

This is the script running in the docker service for the challenge. The script takes in a prime number, and check if its a prime in two ways: the isPrime() function from the Crypto library, and a custom _isPrime() function, which uses the [Miller-Rabin test]() to prove if a number is prime. 

There is a catch though, the script displays the flag, only if the number passes the Miller-Rabin test, but is not actually a prime, i.e., the other isPrime() test fails. Huh? Is this possible?

## Initial Approach

Yes it is! Enter [Carmichael numbers](https://en.wikipedia.org/wiki/Carmichael_number), numbers that aren't actually prime get classified as a prime number due to a feature that I won't talk about because its more math than I can handle. One such number is 561. So let's enter this number and see what happens

```
$ nc 159.65.49.148 30334
Give p: 561
Conditions not satisfied!
```

Oh. It didn't work. I then ran the source code locally on my machine to get a sense of what was happening. After lots of googling and exposure to math and academic papers, here's a brief explanation of the source code.

## Source Code Review

```python
def millerRabin(n, b):
    basis = generate_basis(300)
    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for b in basis:
        x = pow(b, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
```

The test checks the input against multiple bases (spelled as basis here, this did confuse me initially). If the required conditions fail on any given base, the number is considered a composite number and fails the test. These bases can be random numbers, but in our case it is the first 300 prime numbers.

```python
def generate_basis(n):
    basis = [True] * n

    for i in range(3, int(n**0.5) + 1, 2):
        if basis[i]:
            basis[i * i::2 * i] = [False] * ((n - i * i - 1) // (2 * i) + 1)

    return [2] + [i for i in range(3, n, 2) if basis[i]]
```

Certain Carmichael numbers come under the category of [strong pseudoprimes](https://en.wikipedia.org/wiki/Strong_pseudoprime), composite numbers which satisfy some conditions against a specific base. The number 561 is a strong pseudoprime, but not to all bases, which is why it didn't work earlier. We need to look for a number that is a strong pseudoprime to all 300 primes.

## Solution

While searching for potential numbers that would work, I came across this [GitHub gist](https://gist.github.com/keltecc/b5fbd533d2f203e810b43c26ff9d17cc). IT was a script to generate a strong pseudoprime against the first 300 primes, and it gave the prime number at the very end. After this much searching, it felt like finding a treasure chest.

```txt
nc 159.65.49.148 30334
Give p: 99597527340020670697596886062721977401836948352586238797499761849061796816245727295797460642211895009946326533856101876592304488359235447755504083536903673408562244316363452203072868521183142694959128745107323188995740668134018742165409361423628304730379121574707411453909999845745038957688998441109092021094925758212635651445626620045726265831347783805945477368631216031783484978212374792517000073275125176790602508815912876763504846656547041590967709195413101791490627310943998497788944526663960420235802025853374061708569334400472016398343229556656720912631463470998180176325607452843441554359644313713952036867
HTB{c42m1ch431_num8325_423_fun_p53ud0p21m35}
```

Another prime number can be found in [this academic paper](https://www.sciencedirect.com/science/article/pii/S0747717185710425) (I believe this was the intended answer) which I did see but glanced over too quickly to be able to spot the number earlier.

Flag: `HTB{c42m1ch431_num8325_423_fun_p53ud0p21m35}`
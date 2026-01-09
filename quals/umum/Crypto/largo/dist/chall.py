from Crypto.Util.number import getPrime
from libnum import s2n
import secrets
import random

flag = open("flag.txt", "rb").read()
flag = s2n(flag)
p = getPrime(512)
q = getPrime(512)
N = p * q
e = 5
k = 8

cs = [secrets.randbelow(N) for _ in range(k)]
ls = [random.randint(-min(p, q), min(p, q)) for _ in range(k)]

assert all(l != 0 for l in ls), "No zero pls!"
sum_cs = sum([(c * l) % N for c, l in zip(cs, ls)])

cts = []
for c in cs:
    flag ^= c
    cts.append(pow(c, e, N))

with open('output.txt', 'w+') as f:
    f.write(f'{N=}\n')
    f.write(f'{sum_cs=}\n')
    f.write(f'{ls=}\n')
    f.write(f'{cts=}\n')
    f.write(f'{flag=}\n')
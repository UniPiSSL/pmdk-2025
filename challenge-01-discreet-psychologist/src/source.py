from Crypto.Util.number import getPrime
from random import randint
from sympy import primitive_root
import json

FLAG = open("flag.txt","r").read()


def encrypt(plaintext,prime,generator):
    a,b,c,d = [getPrime(10) for _ in range(4)]

    ciphertext = plaintext*a*b*c*d
    for i in range(randint(100,400)):
        ciphertext = pow(generator,ciphertext,prime)

    return (ciphertext, [a,b,c,d])


out = []

prime = getPrime(48)
generator = primitive_root(prime)

for index in range(len(FLAG)):
    out.append(encrypt(ord(FLAG[index]),prime,generator))

challenge = {"outputs" : out, "prime" : prime, "generator" : generator}

open("output.txt", "w").write(json.dumps(challenge))

from secret import e, FLAG
from Crypto.Util.number import isPrime, getPrime, bytes_to_long, long_to_bytes, GCD
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
import secrets, random

assert isPrime(e) and not (e-1) & 1 and isPrime(e-1)

E = [e] + [secrets.randbits(16) for _ in range(13)]
random.shuffle(E)

class RSA:
	def __init__(self, bits):
		p = getPrime(bits)
		q = getPrime(bits)
		self.n = p * q
    
	def encrypt(self, m):
		c = secrets.choice(E)
		return pow(m, c, self.n)

RSAs = [RSA(512) for _ in range(65)]

m = bytes_to_long(FLAG)

encs = [rsa.encrypt(m) for rsa in RSAs]
N = [rsa.n for rsa in RSAs]

with open('output.txt', 'w') as f:
	f.write(f'{encs = }\n')
	f.write(f'{N = }')
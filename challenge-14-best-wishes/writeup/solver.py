from Crypto.Util.number import GCD, bytes_to_long, long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha256

def factor(n, e, d):
    """http://crypto.stackexchange.com/a/25910/17884
    
    n - modulus
    e - public exponent
    d - private exponent
    returns - (p, q) such that n = p*q
    """
    from random import randint

    while True:
        z = randint(2, n - 2)
        k, x = 0, e * d - 1

        while not x & 1:
            k += 1
            x >>= 1

        t = pow(z, x, n)
        if t == 1 or t == (n-1):
            continue

        bad_z = False
        for _ in range(k):
            u = pow(t, 2, n)

            if u == -1 % n:
                bad_z = True
                break

            if u == 1:
                p = GCD(n, t-1)
                q = GCD(n, t+1)
                assert n == p * q
                return p, q
            else:
                t = u

        if bad_z:
            continue

exec(open('output.txt').read())

e = 65537

msgs = [bytes_to_long(b'Good luck!'), bytes_to_long(b'You need it!')]

n = GCD(msgs[0] ** e - enc_msgs[0], msgs[1] ** e - enc_msgs[1])

for i in range(2, 10**5):
	if n % i == 0:
		n //= i

print(f'{n = }')

p, q = factor(n, e, d)

assert n == p * q

key = sha256((str(p) + str(q)).encode()).digest()
cipher = AES.new(key, AES.MODE_CBC, iv=bytes.fromhex(iv))

print(unpad(cipher.decrypt(bytes.fromhex(enc_flag)), 16))
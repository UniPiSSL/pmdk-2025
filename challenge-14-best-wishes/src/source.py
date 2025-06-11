from secret import FLAG
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes, GCD
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256

p = getPrime(768)
q = getPrime(768)
e = 65537
n = p * q
phi = (p-1) * (q-1)

d = pow(e, -1, phi)

key = sha256((str(p) + str(q)).encode()).digest()
cipher = AES.new(key, AES.MODE_CBC)
enc_flag = cipher.encrypt(pad(FLAG, 16)).hex()

enc_msgs = [pow(bytes_to_long(m), e, n) for m in [b'Good luck!', b'You need it!']]

iv = cipher.iv.hex()
with open('output.txt', 'w') as f:
	f.write(f'{d = }\n')
	f.write(f'{enc_msgs = }\n')
	f.write(f'{iv = }\n')
	f.write(f'{enc_flag = }\n')
from pwn import *
import itertools
from hashlib import md5,sha256,sha1
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b


def bxor(a, b, c):
    return bytes(x ^ y ^ z for x, y, z in zip(a, b, c))

pool = "0123456789abcdef"
combinations = itertools.product(pool, repeat=5)

Rainbow_Table = {}

counter = 0
for combo in combinations:
    print(f"remaining {16**5 - counter}")
    Hash_Input = ''.join(combo)
    Rainbow_Table[sha1(Hash_Input.encode()).hexdigest()] = Hash_Input
    Rainbow_Table[sha1(bxor(sha256(Hash_Input.encode()).digest(),md5(Hash_Input.encode()).digest(),sha1(Hash_Input.encode()).digest())).hexdigest()] = Hash_Input
    Rainbow_Table[sha1(sha256(md5(Hash_Input.encode()).digest()).digest()).hexdigest()] = Hash_Input
    Rainbow_Table[sha1(l2b(b2l(md5(Hash_Input.encode()).digest()[:8]) << 32) + l2b(b2l(md5(Hash_Input.encode()).digest()[8:]) << 52)).hexdigest()] = Hash_Input
    counter += 1

r = remote("localhost", 1337)
print(r.recvuntil(b"Suguru Geto\r\n\r\n"))
while True:
    rec = r.recvline()
    print(rec)
    if b"FLAG{" in rec:
        print(rec)
        exit()
    Hash = rec.split(b" = ")[1].strip().decode()
    r.recvuntil(b" > ")
    r.sendline(Rainbow_Table[Hash].encode())




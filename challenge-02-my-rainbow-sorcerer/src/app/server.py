from hashlib import md5,sha256,sha1
from random import randint
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b
import time

def bxor(a, b, c):
    return bytes(x ^ y ^ z for x, y, z in zip(a, b, c))

pool = "0123456789abcdef"

def Challenge():
    input = "".join(pool[randint(0,len(pool)-1)] for _ in range(5))
    
    b0,b1 = [randint(0,1) for _ in range(2)]
    if int(f"{b0}{b1}",2) == 0:
        Grade4_CSpirit = sha1(input.encode()).hexdigest()
        return Grade4_CSpirit, input
    elif int(f"{b0}{b1}",2) == 1:
        Grade2_CSpirit = sha1(bxor(sha256(input.encode()).digest(),md5(input.encode()).digest(),sha1(input.encode()).digest())).hexdigest()
        return Grade2_CSpirit, input
    elif int(f"{b0}{b1}",2) == 2:
        Grade1_CSpirit = sha1(sha256(md5(input.encode()).digest()).digest()).hexdigest()
        return Grade1_CSpirit, input
    else:
        SpecialGrade_CSpirit = sha1(l2b(b2l(md5(input.encode()).digest()[:8]) << 32) + l2b(b2l(md5(input.encode()).digest()[8:]) << 52)).hexdigest()
        return SpecialGrade_CSpirit, input

print("Do you have the Hash because you know the Input?")
print("Or you have the Input because you know the Hash ~ Suguru Geto\n")

for _ in range(500):
    Hash, Input = Challenge()
    print(f"What is the Input used in this Satoru = {Hash}")
    start_time = time.time()
    guess = input("Input > ")
    elapsed_time = time.time() - start_time
    if elapsed_time > 5:
       print("Time's up! You are late as always Satoru...")
       exit()
    if guess != Input:
        print("Well Well Well...This is it Satoru...You lost!")
        exit()
    
print(f"Nah, You'd Win...{open("flag.txt","r").read()}")

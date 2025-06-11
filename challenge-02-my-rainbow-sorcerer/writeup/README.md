# My Rainbow Sorcerer Write-Up

| Δοκιμασία | My Rainbow Sorcerer |
| :------- | :----- |
| Δυσκολία | Εύκολη |
| Κατηγορία | Κρυπτογραφία (Cryptography) |
| Λύσεις | 13 |
| Πόντοι | 420 |


## Περιγραφή Δοκιμασίας

``` 
Can you beat Suguru Geto?
```

### Source Code

```py
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
```

## Επίλυση
### Με μια πρώτη ματιά

Έχουμε μια λούπα που επαναλαμβάνεται 500 φορές.
Σε κάθε επανάληψη μας δίνεται ένα hash και πρέπει να δώσουμε μέσω ποιανού input δημιουργήθηκε αυτό το hash.
Αν δώσουμε λάθος απάντηση η σύνδεση μας στον server κλείνει και πρέπει να επαναλάβουμε την διαδικασία.

Πώς γίνεται generate όμως το input?

### Ανάλυση - Εύρεση ευπάθειας - Exploitation


```py
pool = "0123456789abcdef"


input = "".join(pool[randint(0,len(pool)-1)] for _ in range(5))
```

Παρατηρούμε ότι έχουμε ένα σύνολο χαρακτήρων, οι οποίοι είναι όλοι οι χαρακτήρες του δεκαεξαδικού συστήματος. Από αυτούς επιλέγονται τυχαία 5.

Επομένως το input σε κάθε επανάληψη θα είναι 5 τυχαίοι χαρακτήρες από το σύνολο `0123456789abcdef`.


```py
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
```

Στην συνέχεια ο server αποθηκεύει σε δύο μεταβλητές τυχαία είτε το `0` είτε το `1` και το μετατρέπει από δυαδικό σε δεκαδικό αριθμό. Άρα έχουμε:

`00` : `0`

`01` : `1`

`10` : `2`

`11` : `3`


Βάση του αποτελέσματος:

`0` : Επιστρέφει το `sha1` hash του input

`1` : Υπολογίζει το `md5`,`sha1`,`sha256` και τα κάνει `xor` μεταξύ τους και επιστρέφει το `sha1` του αποτελέσματος

`2` : Επιστρέφει το `sha1` του `sha256` του `md5` του input.

`3` : Υπολογίζει το `md5` hash του μηνύματος και το χωρίζει στην μέση. Στην συνέχεια αφού τα μετατρέψει σε αριθμό μετατοπίζει το πρώτο μισό κατά `32` bit αριστερά και το δεύτερο μισό κατά `52` bit αριστερά


Οπότε πώς εμείς μπορούμε να ξέρουμε από το hash που μας δίνεται μόνο από το hash του;

Δεδομένου ότι σε μια hash function όταν μπαίνει το ίδιο input βγαίνει το ίδιο output μπορούμε να κατασκευάσουμε ένα `Rainbow Table`. 

Μια `Rainbow Table` είναι ένας πίνακας προ-υπολογισμένων hash για μια σειρά από πιθανές τιμές. Κάθε γραμμή του πίνακα περιέχει έναν κωδικό και το αντίστοιχο hash του.


Δεδομένου ότι έχουμε ένα σύνολο 16 πιθανόν γραμμάτων και θέλουμε να φτιάξουμε ένα `Rainbow Table` για όλους τους συνδυασμούς του, θα κατασκευάσουμε έναν πίνακα `16`<sup>`5`</sup> = `1048576`


Αφότου κατασκευάσουμε το `Rainbow Table` συνδεόμαστε στον server και βάση του `hash` που μας δίνεται δίνουμε το αντίστοιχο input απο το `Rainbow Table`.
### Solver


```py
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
```

## Σημαία

```
FLAG{https://www.youtube.com/watch?v=bU2EvRBUmxc}
```

# Discreet Psychologist Write-Up

| Δοκιμασία | Discreet Psychologist |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Κρυπτογραφία (Cryptography) |
| Λύσεις | 20 |
| Πόντοι | 149 |


## Περιγραφή Δοκιμασίας

``` 
My psychologist's prescription does not make sense. I wish I could find the log-ic behind it..
```

### Source Code

```py
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
```

### Output Data

 `output.txt` με τους κρυπτογραφημένους χαρακτήρες του `FLAG` και τις παραμέτρους `a,b,c,d`.

## Επίλυση
### Με μια πρώτη ματιά

Έχουμε έναν `Prime` 48 bits
Τον γεννήτορα της ομάδας `generator` (ο Γεννήτορας της ομάδας σε μια δύναμη mod τον `Prime` κάνει "generate" στοιχεία της ομάδας)


Ο κώδικας χρησιμοποιεί την σχέση `generator`<sup>`char`</sup> % `Prime`
σε μια λούπα από 100 έως 400 όπου char είναι ο κάθε χαρακτήρας του `FLAG` μας πολλαπλασιασμένος με 4 τυχαίους πρώτους αριθμούς των 10 bit.

char = `Flag_char * a * b * c * d`


### Ανάλυση - Εύρεση ευπάθειας - Exploitation

Παρατηρούμε ότι ο πρώτος αριθμός που χρησιμοποιείται για την κρυπτογράφηση του I-οστού χαρακτήρα του `FLAG` είναι πολύ μικρός. 

Όταν έχουμε μια σχέση όπως `generator`<sup>`char`</sup> % `Prime` και ψάχνουμε να βρούμε την δύναμη που υψώθηκε το `g % p` ονομάζεται πρόβλημα διακριτού λογαρίθμου (descrete log problem) και είναι αδύνατο να λυθεί για πρώτους αριθμούς πολλών bits πχ 256,512 κ.α.

Ωστόσο, όπως αναφέραμε ο Prime που χρησιμοποιείται εδώ είναι μόλις 48 bits. 

Πράγμα που κάνει τον διακριτό λογάριθμο επιλύσιμο.


Επομένως για κάθε χαρακτήρα μπορούμε να υπολογίσουμε τον διακριτό λογάριθμο.

Ωστόσο, η σχέση  `generator`<sup>`char`</sup> % `Prime` έχει επαναληφθεί σε μια λούπα από 100 έως 400 φορές. Αυτό σημαίνει ότι δεν μπορούμε να ξέρουμε ακριβώς πόσες φορές πρέπει να υπολογίσουμε τον διακριτό λογάριθμο ώστε να έχουμε ανακτήσει το

char = `Flag_char * a * b * c * d`


Το μόνο που ξέρουμε είναι ότι το εύρος των επαναλήψεων μπορεί να είναι από 100 φορές μέχρι 400. Έχοντας λοιπόν τα `a,b,c,d` μπορούμε να κάνουμε factor το αποτέλεσμα του διακριτού λογάριθμου και αν οι παράγοντες αποτελούνται από τα `a,b,c,d` και κάτι ακόμα στο εύρος 32-126 (όλοι οι printable characters) τότε σημαίνει ότι έχουμε βρει τον σωστό διακριτό λογάριθμο και επομένως έχουμε ανακτήσει το σωστό γράμμα του `FLAG`.

Επαναλαμβάνουμε την ίδια διαδικασία για όλα τα γράμματα του `FLAG`

### Solver


```py

from sympy import discrete_log,factorint
import json

challenge = json.loads(open("output.txt","r").read())

outputs = challenge['outputs']
prime = challenge['prime']
generator = challenge['generator']

def factors(ciphertext,multi):
    a,b,c,d = multi
    fact = list(factorint(ciphertext).keys())
    
    if all(x in fact for x in [a, b, c, d]):
        return ciphertext//(a*b*c*d),True
    else:
       return 0, False


def decrypt(char):
    ciphertext = char[0]
    for i in range(400):
        ciphertext = discrete_log(prime,ciphertext,generator)
        flag_char, boolean = factors(ciphertext,char[1])
        if boolean == True:
           break
    return flag_char

FLAG = ""


for char in outputs:
    FLAG += chr(decrypt(char))
    print(FLAG)
```

## Σημαία

```
FLAG{https://www.youtube.com/watch?v=RBtlPT23PTM}
```

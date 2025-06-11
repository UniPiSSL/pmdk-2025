# There was an incident! Write-Up

| Δοκιμασία | There was an incident! |
| :------- | :----- |
| Δυσκολία | Εύκολη |
| Κατηγορία | Ψηφιακή Εγκληματολογία (Forensics) |
| Λύσεις | 32 |
| Πόντοι | 100 |


## Περιγραφή Δοκιμασίας

``` 
Ω Θεέ μου... συνέβη ένα περιστατικό! Κάποιος απέκτησε πρόσβαση στον διακομιστή μας και κρυπτογράφησε τα αρχεία του απόρρητου έργου μας! Χρειαζόμαστε τη βοήθειά σου!

Συνδέσου στον διακομιστή χρησιμοποιώντας τα: `support:password123`.
```

## Επίλυση
### Με μια πρώτη ματιά

Συνδεόμαστε στον διακομιστή χρησιμοποιώντας το όνομα χρήστη και τον κωδικό που μας δόθηκαν και την IP διεύθυνση που για το instance που ξεκινήσαμε στην πλατφόρμα του διαγωνισμού:
```
ssh support@10.0.0.1
# Κωδικός: password123
```

Αφού συνδεθούμε και κοιτάξουμε τα αρχεία του server, καταλαβαίνουμε πως ο στόχος αυτής της δοκιμασίας είναι να διερευνήσουμε το περιστατικό στον απομακρυσμένο διακομιστή και να ανακτήσουμε (αν μπορούμε) τα κρυπτογραφημένα αρχεία, εντοπίζοντας το flag (σημαία) που έχει αποθηκευτεί κάπου στα δεδομένα.
```
support@0a876cfe759b:~$ ls
documents   readme-your-data-were-encrypted.txt
support@0a876cfe759b:~$ cat readme-your-data-were-encrypted.txt
Transfer 2 Bitcoin to our address 1JC92RtUqNtvd3ZghWTEj3FyxuGfPRjpBW and we will give you the password.
```

### Ανάλυση

Χρησιμοποιούμε την εντολή `history` για να δούμε τις πρόσφατες ενέργειες που έγιναν στο σύστημα:
```
support@0a876cfe759b:~$ history
    1  ls
    2  ls ./documents
    3  zip --password 3ikVdfMnNXcSPsdhjUe3Twxr1gXuTWVi -r encrypted_files.zip ./documents/
    4  rm -rf ./documents
    5  echo "Transfer 2 Bitcoin to our address 1JC92RtUqNtvd3ZghWTEj3FyxuGfPRjpBW and we will give you the password." > ./readme-your-data-were-encrypted.txt
    6  exit
    7  ls
    8  history
```

Παρατηρήσεις από το ιστορικό των εντολών που εκτελέστηκαν:
- Στη γραμμή 3, βλέπουμε ότι δημιουργήθηκε ένα zip αρχείο με κωδικό πρόσβασης.
- Ο κωδικός αυτός εμφανίζεται ξεκάθαρα στην εντολή: `3ikVdfMnNXcSPsdhjUe3Twxr1gXuTWVi`
- Στη γραμμή 4, τα αρχικά αρχεία διαγράφηκαν.
- Στη γραμμή 5, δημιουργείται ένα αρχείο εκβιασμού που ζητά λύτρα σε Bitcoin.

Αφού έχουμε τον κωδικό, μπορούμε να προχωρήσουμε στην ανάκτηση των κρυπτογραφημένων αρχείων.

Αποσυμπιέζουμε λοιπόν το αρχείο `encrypted_files.zip` χρησιμοποιώντας τον κωδικό που βρήκαμε στο ιστορικό:
```
support@0a876cfe759b:~$ unzip -P 3ikVdfMnNXcSPsdhjUe3Twxr1gXuTWVi encrypted_files.zip
Archive:  encrypted_files.zip
   creating: documents/
  inflating: documents/confidential.odt
  inflating: documents/schematics.png
 extracting: documents/flag.txt
```

Στην συνέχεια, μπορούμε να εκτυπώσουμε την σημαία από το αρχείο `flag.txt`:
```
support@0a876cfe759b:~$ cat documents/flag.txt
FLAG{c4lm_d0wn!...I_r3c0vered_y0ur_F1L35!}
```

## Σημαία

```
FLAG{c4lm_d0wn!...I_r3c0vered_y0ur_F1L35!}
```

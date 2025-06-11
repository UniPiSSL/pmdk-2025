| Δοκιμασία | Ascent Main |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Αντίστροφη Mηχανική (Reverse Engineering) |
| Λύσεις | 9 |
| Πόντοι | 520 |

## Επίλυση 
Η δοκιμασία αποτελείται από ένα εκτελέσιμο αρχείο. 
Αρχικά ας πάρουμε μερικές πληροφορίες για εκείνο.  
`` main: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped``

* 64 bit executable 
* statically linked
* not striped

Συμπεραίνουμε ότι το εκτελέσιμο μας δεν είναι stripped άρα έχουμε κάποιες πληροφορίες για τα αρχικά ονόματα των συναρτήσεων και των μεταβλητών.
Τώρα ας δούμε την συμπεριφορά του.

```
./main
Lets see if you are good enough to solve my exams!
Enter the magic world:
FLAG{test}
Nope. Seems that you did not study enough.
```
Από ότι φαίνεται πρέπει να εισάγουμε τον σωστό κωδικό έτσι ώστε να πάρουμε το αντίστοιχο σωστό μήνυμα.
Χρησιμοποιούμε έναν dissasembler της επιλογής μας για να αναλύσουμε τον κώδικα του. 
![image](https://github.com/user-attachments/assets/26f70c65-65b2-4ff5-908b-1258dcc817ce)

Σαν πρώτη όψη φαίνεται αρκετά σύντομο. Ας ξεκινήσουμε να το αναλύουμε!     

```asm
mov     edi, 1          ; fd
mov     rsi, offset Welcome_msg ; buf
mov     edx, 33h ; '3'  ; count
mov     eax, 1
syscall                 ; LINUX - sys_write
mov     eax, 0Ah
mov     rdi, offset actual_checker
and     rdi, 0FFFFFFFFFFFFF000h ; start
mov     esi, 1000h      ; len
mov     edx, 7          ; addr
syscall                 ; LINUX - sys_mprotect
```
Το πρόγραμμα χρησιμοποιεί syscalls για την αλληλεπίδραση του με το περιβάλλον. Έχουμε την δυνατότητα να δούμε το functionality του κάθε syscall με τον τρόπο τον οποίο σετάρονται οι καταχωρητές.
Για παράδειγμα:
* rax : syscall id
* rdi : first argument
* rsi : second argument
* rdx : third argument  

Έτσι έχοντας στην διάθεση μας ένα linux syscall [table](https://chromium.googlesource.com/chromiumos/docs/+/master/constants/syscalls.md)
Φαίνεται ότι στην πρώτη περίπτωση καλείται η sys_write, η οποία θα εκτυπώσει το welcome msg `"Lets see if you are good enough to solve my exams!"`  

Στην συνέχεια χρησιμοποιείται η mprotect η οποία αλλάζει τα permissions μιας μεταβλητής η οποία ζει μέσα στο .data segment και κάνει την περιοχή executable.
Τέλος, καλείται η [sys_ptrace](https://man7.org/linux/man-pages/man2/ptrace.2.html) η οποία ελέγχει αν το πρόγραμμα εκτελείται από κάποιον debugger.  

Στην περίπτωση που το process γίνεται debug εκτυπώνεται το μήνυμα `"Seems you are trying to cheat."` και τερματίζει το πρόγραμμα 

Σε κάθε άλλη περίπτωση το πρόγραμμα ακολουθεί ένα διαφορετικό path στο οποίο φαίνεται να γίνεται decrypt το περιεχόμενο της καθολικής μεταβλητής `actual_checker`
```asm
mov     rdi, offset actual_checker
l1:                                     ; CODE XREF: _start+72↓j
mov     al, [rdi+rsi]
xor     al, 69h
mov     [rdi+rsi], al
inc     rsi
cmp     rsi, 0D4h
jnz     short l1
```
Ο δρόμος πλέον που πρέπει να ακολουθήσουμε είναι να κάνουμε bypass το antidebug technique και να πηδήξουμε στον decrypted checker!
Υπάρχουν πολλοί τρόποι για να το κάνουμε αυτό. Εγώ θα προτιμήσω να αλλάξω το περιεχόμενο που επιστρέφει η ptrace σε 0 για να περάσει το check.
Μετά το  
```asm 
jmp     actual_checker
```  
Φαίνεται πάλι η χρήση ψευδοκώδικα να μην μας βοηθάει 
![image](https://github.com/user-attachments/assets/60992cf5-4197-4680-ae3c-3721acdb7fea)
οπότε ας συνεχίσουμε να διαβάζουμε assembly.
η πρώτη syscall που συναντάμε εκτυπώνει το μήνυμα για να εισάγουμε τον κωδικό  
(όπως είπαμε πριν τα arguments μπαίνουν στους καταχωρητές όπως παρακάτω)
```asm
mov     rsi, offset prompt ; buf
mov     edx, 18h        ; count
syscall
```

και η δεύτερη είναι η sys_read η οποία διαβάζει 28 χαρακτήρες απο τον χρήστη.
```asm
mov     edi, 0                  ; fd
rsi, ds:4020C8h                 ; buf
mov     edx, 28                 ; count
syscall
```
Συνεχίζοντας, εμφανίζεται μια λούπα η οποία περπατάει το input μας και εφαρμόζει κάποια operations πάνω του αλλά και συγκρίνει τον κάθε χαρακτήρα με έναν αντίστοιχο από ένα byte array  
`73 7D 08 72 4E 08 66 7C 6A 28 66 6A 64 7B 75 06 67 08 65 65 06 75 6A 18 06 06 02 4C`  
Ο αλγόριθμος κρυπτογραφησης φαίνεται να παίρνει κάθε χαρακτήρα μας να προσθέτει 1, να αφαιρεί 3 και να εφαρμόζει την πράξη xor με τον αριθμό 0x37.
```asm
loc_40210A:
add     cl, 1
sub     cl, 3
xor     cl, 37h
cmp     cl, [rbx]
jnz     short loc_40214A
```  

Σε περίπτωση που βρεθεί ένας χαρακτήρας ο οποίος δεν ικανοποίει την συνθήκη τότε το πρόγραμμα τερματίζει εκτυπώνοντας  
`Nope. Seems that you did not study enough.'` 
αλλιώς νικήσαμε.  
Έτσι γράφουμε ένα python script αντιστρέφοντας τις πράξεις 
```python
enc = [0x73,0x7d,0x08,0x72,0x4e,0x08,0x66,0x7c,0x6a,0x28,0x66,0x6a,0x64,0x7b,0x75,0x06,0x67,0x08,0x65,0x65,0x06,0x75,0x6a,0x18,0x06,0x06,0x02,0x4c]

for i in enc:
    i ^= 0x37
    i += 3 
    i -= 1
    print(chr(i), end="")
```
Και έτσι παίρνουμε τον σωστό κωδικό  
`FLAG{ASM_!S_UND3RATT3D_1337}`

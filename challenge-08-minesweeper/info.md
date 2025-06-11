# Info on how the flag was encrypted

The flag was XORed with a sha512 message made from various game variables.

You can use the following code to change the flag:
```javascript
let key = 'Minesweeper_true_32_true_32_512_0_You Win!🎉'
let flag = 'FLAG{1_tH1nK_i_g0t_eN0ugh_G4me_H4ck1nG_FuN_4_tOdAY!}';
let h = (sha512(key + '_1') + sha512(key + '_2') + sha512(key + '_3')).match(/../g).map((x) => parseInt(x, 16)).slice(0, 52);
let s = Uint8Array.from(new TextEncoder().encode(flag), (v, i) => v ^ h[i]);
console.log(s.toString(s));
console.log(s.length);
```

The source code was obfuscated using https://obfuscator.io/

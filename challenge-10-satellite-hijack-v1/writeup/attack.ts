// The hash function
const hashed = (data: string) => Bun.hash(data).toString();

// Hash to break
const targetHash = "2842816338533097556";
console.log('Target Hash:', targetHash);

// Loop through all possible combinations
process.stdout.write("Bruteforcing [0%]");
for (let i = 0; i <= 999_999_999; i++) {
    if (hashed(i.toString()) == targetHash) {
        console.log(`\nMatch found: ${i}`);
        break;
    }
    if (i % 10_000_000 === 0) {
        process.stdout.write(`\rBruteforcing [${Math.round(i * 100/999_999_999)}%]`);
    }
}
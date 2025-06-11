from itertools import combinations
from gmpy2 import iroot
from sympy.ntheory.modular import crt
from tqdm import tqdm
from Crypto.Util.number import long_to_bytes

e = 3

exec(open('output.txt').read())

for comb in tqdm(combinations(range(len(N)), r=e)):
    selected_N = [N[i] for i in comb]
    selected_encs = [encs[i] for i in comb]
    sol, pr = crt(selected_N, selected_encs)
    m, b = iroot(sol, e)
    if b:
        print(long_to_bytes(m))
        break
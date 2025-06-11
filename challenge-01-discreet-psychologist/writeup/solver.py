
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


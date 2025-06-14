SYS_EXIT  equ 1
STDIN     equ 0
STDOUT    equ 1

section .bss
   buffer resb 28
   letter resb 1

section	.data

Welcome_msg db 'Lets see if you are good enough to solve my exams!', 0xa

prompt db 'Enter the magic world: ', 0xa

Win_msg db 'Congrats! GRADE:10', 0xA

False_msg db 'Nope. Seems that you did not study enough.', 0xA

Antidebug_err_msg db 'Seems you are trying to cheat.', 0xa

len equ $ - Welcome_msg

nothing_here: db 0x73,0x7d,0x08,0x72,0x4e,0x08,0x66,0x7c,0x6a,0x28,0x66,0x6a,0x64,0x7b,0x75,0x06,0x67,0x08,0x65,0x65,0x06,0x75,0x6a,0x18,0x06,0x06,0x02,0x4c,0xc9 ; enc flag
actual_checker: db 0x58, 0xa9, 0x0f, 0xea, 0xa9, 0x68, 0xd6, 0x68, 0x69, 0x69, 0x69, 0x21, 0xd7, 0x5a, 0x49, 0x29, 0x69, 0x69, 0x69, 0x69, 0x69, 0xd3, 0x71, 0x69, 0x69, 0x69, 0x66, 0x6c, 0x58, 0xa9, 0xd6, 0x69, 0x69, 0x69, 0x69, 0x21, 0xe4, 0x5d, 0x4c, 0xa1, 0x49, 0x29, 0x69, 0xd3, 0x75, 0x69, 0x69, 0x69, 0x66, 0x6c, 0x21, 0x58, 0xa0, 0xe3, 0x67, 0xe9, 0x80, 0x68, 0x21, 0xe4, 0x75, 0x4c, 0xc1, 0x49, 0x29, 0x69, 0x21, 0x58, 0xa9, 0xe9, 0xa8, 0x6b, 0xe9, 0x80, 0x6a, 0xe9, 0x98, 0x5e, 0x53, 0x62, 0x1c, 0x5a, 0x21, 0x96, 0xaa, 0x21, 0x96, 0xaf, 0xe3, 0x67, 0x0f, 0x96, 0xa9, 0x0f, 0xea, 0x91, 0x75, 0x1d, 0x6b, 0x8b, 0x89, 0x58, 0xa9, 0xea, 0xa9, 0x68, 0xd6, 0x68, 0x69, 0x69, 0x69, 0x21, 0xd7, 0x22, 0x49, 0x29, 0x69, 0x69, 0x69, 0x69, 0x69, 0xd3, 0x7a, 0x69, 0x69, 0x69, 0x66, 0x6c, 0x21, 0x58, 0xa9, 0x82, 0x4a, 0x21, 0x58, 0xa9, 0x21, 0xea, 0xa9, 0x68, 0xd6, 0x68, 0x69, 0x69, 0x69, 0x21, 0xd7, 0x37, 0x49, 0x29, 0x69, 0x69, 0x69, 0x69, 0x69, 0xd3, 0x42, 0x69, 0x69, 0x69, 0x66, 0x6c, 0x21, 0xea, 0x81, 0x68, 0x82, 0x69, 0xd1, 0x55, 0x69, 0x69, 0x69, 0x66, 0x6c, 0x58, 0xa9, 0xd1, 0x68, 0x69, 0x69, 0x69, 0xd6, 0x68, 0x69, 0x69, 0x69, 0x21, 0xd7, 0xe0, 0x49, 0x29, 0x69, 0x69, 0x69, 0x69, 0x69, 0xd3, 0x76, 0x69, 0x69, 0x69, 0x66, 0x6c, 0xd6, 0x68, 0x69, 0x69, 0x69, 0x82, 0xbc, 0xf9


section	.text
   global _start

_start:
   mov  rdi, 1
   mov  rsi, Welcome_msg ; prints the welcome msg
   mov  rdx, 51
   mov  eax, 1
   syscall

   mov rax, 0xa
   mov rdi, actual_checker   ; making the .data segment executable  
   and rdi, -0x1000   ; aligning page 
   mov rsi, 0x1000                           
   mov rdx, 0x7
   syscall

   mov eax,101
   xor rdi,rdi
   xor rsi,rsi
   syscall
   cmp rax, 0     ; antidebug check with ptrace
   jne detected
   
   xor rax,rax
   xor rsi,rsi
   mov rdi, actual_checker

l1:   
   mov al, [rdi+rsi]
   xor al, 0x69
   mov [rdi+rsi], al    ; decrypting actual checker
   
   inc rsi
   cmp rsi, 212
   jne l1
   
   jmp actual_checker ; jumping into actual flag checker

exit:
    mov  eax,60    ; exit 
    syscall

detected:
   xor  eax,eax
   mov  eax,1
   mov  rdi,STDOUT  ; Antidebug_err_msg
   mov  rsi,Antidebug_err_msg
   mov  edx,31
   syscall
   mov  rdi,1
   jmp exit
   nop
   
section .note.GNU-stack

# MaxFucktor
Yet another BF compiler, writtern in pure Python.


```asm
global _start


section .data
    memory: times 32768 db 0


section .text
_start:
    mov r10, memory
    jmp run
exit:
    mov rax, 60
    mov rdi, 0
    syscall
do_write:
    mov rax, 1
    mov rdi, 1
    lea rsi, [r10]
    mov rdx, 1
    syscall
    ret
do_read:
    mov rax, 0
    mov rdi, 0
    lea rsi, [r10]
    mov rdx, 1
    syscall
    ret
run:
    add byte [r10], byte 10
    l1:
    cmp byte [r10], byte 0
    je l2
    add r10, 1
    add byte [r10], byte 7
    add r10, 1
    add byte [r10], byte 10
    add r10, 1
    add byte [r10], byte 3
    add r10, 1
    add byte [r10], byte 1
    sub r10, 4
    sub byte [r10], byte 1
    jmp l1
    l2:
    add r10, 1
    add byte [r10], byte 2
    call do_write
    add r10, 1
    add byte [r10], byte 1
    call do_write
    add byte [r10], byte 7
    call do_write
    call do_write
    add byte [r10], byte 3
    call do_write
    add r10, 1
    add byte [r10], byte 2
    call do_write
    sub r10, 2
    add byte [r10], byte 15
    call do_write
    add r10, 1
    call do_write
    add byte [r10], byte 3
    call do_write
    sub byte [r10], byte 6
    call do_write
    sub byte [r10], byte 8
    call do_write
    add r10, 1
    add byte [r10], byte 1
    call do_write
    jmp exit
```
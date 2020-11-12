# MaxFucktor
Yet another BF compiler, writtern in pure Python.

## Meta
This repo contains a fairly straight forward, yet complete implementation of BF to NASM (YASM) translator.  The resulting code is Linux specific, as it does IO via syscalls. 

## Installation
As usual:
```bash
$ (venv): python setup.py install
$ (venv): sudo apt install yasm 
```

## Hello world
The `src` folder contains handful of BF programs. Use `build.sh` script to get an executable:
```bash
$: ./build.sh src/helloworld.b
$: ./res
Hello World!
$:
```

## ASM quality
Compiler is ok'ish. I've done some profiling with `valgrind`, which didn't show any major branch misprediction (around 5~7% avg) and pretty much no CPU cache misses. Here's a resulting `ASM` for the `helloworld.b` program:

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

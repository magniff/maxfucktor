# MaxFucktor
Yet another BF compiler, written in pure Python.

## Meta
This repo contains a fairly straight forward, yet complete implementation of BF to NASM (YASM) translator.  The resulting code is Linux specific, as it does IO via syscalls. 

## Installation
As usual:
```bash
$ (venv): python setup.py install
$ (venv): sudo apt install yasm 
```

## Hello world
The `src` folder contains handful of BF programs.  Use `build.sh` script to get an executable:
```bash
$: ./build.sh src/helloworld.b
$: ./res
Hello World!
$:
```

## ASM quality
Compiler is doing ok'ish job.  I've done some profiling with `valgrind`, which didn't show any major branch misprediction (around 5~7% avg) and pretty much no CPU cache misses.  Here's a resulting `ASM` for the `helloworld.b` program:
```asm
global _start


section .data
    memory: times 32768 db 0


section .text
_start:
    mov rsi, memory
    mov rdx, 1 ;; rdx wont change during the runtime
    mov rdi, 1 ;; rdi represents an io descriptor, typically 1 or 0
    jmp run
exit:
    mov rax, 60
    mov rdi, 0
    syscall
run:
    add byte [rsi], byte 10
    l1:
    cmp byte [rsi], byte 0
    je l2
    add rsi, 1
    add byte [rsi], byte 7
    add rsi, 1
    add byte [rsi], byte 10
    add rsi, 1
    add byte [rsi], byte 3
    add rsi, 1
    add byte [rsi], byte 1
    sub rsi, 4
    sub byte [rsi], byte 1
    jmp l1
    l2:
    add rsi, 1
    add byte [rsi], byte 2
    mov rax, 1
    syscall
    add rsi, 1
    add byte [rsi], byte 1
    mov rax, 1
    syscall
    add byte [rsi], byte 7
    mov rax, 1
    syscall
    mov rax, 1
    syscall
    add byte [rsi], byte 3
    mov rax, 1
    syscall
    add rsi, 1
    add byte [rsi], byte 2
    mov rax, 1
    syscall
    sub rsi, 2
    add byte [rsi], byte 15
    mov rax, 1
    syscall
    add rsi, 1
    mov rax, 1
    syscall
    add byte [rsi], byte 3
    mov rax, 1
    syscall
    sub byte [rsi], byte 6
    mov rax, 1
    syscall
    sub byte [rsi], byte 8
    mov rax, 1
    syscall
    add rsi, 1
    add byte [rsi], byte 1
    mov rax, 1
    syscall
    jmp exit
```

### Performance
> Not great, not terrible. We did everything right. (c)

```bash
$ multitime -q -n 50 "./hanoi"
            Mean        Std.Dev.    Min         Median      Max
real        0.056       0.012       0.041       0.055       0.083       
user        0.053       0.010       0.038       0.052       0.077       
sys         0.003       0.003       0.000       0.004       0.008
```

```bash
$ multitime -q -n 50 "./mandelbrot" 
            Mean        Std.Dev.    Min         Median      Max
real        0.894       0.018       0.873       0.886       0.966       
user        0.893       0.017       0.873       0.885       0.966       
sys         0.001       0.002       0.000       0.000       0.008
```

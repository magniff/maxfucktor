#!/bin/sh
bfcompiler -i $1 -t templates/nasm_template.jinja > res.asm &&
yasm -f elf64 -g dwarf2 -o res.o res.asm && ld res.o -o res

from pwn import *
from sys import *

# context.terminal = ["tmux", "splitw", "-h"]
#elf = context.binary = ELF("./d8")
p = process(["./d8", "--allow-natives-syntax", "solver.js", "--shell"])
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

HOST = ''
PORT = 1

cmd = """
b*main
"""
if(argv[1] == 'gdb'):
    gdb.attach(p,cmd)
elif(argv[1] == 'rm'):
    p = remote(HOST,PORT)

p.interactive()
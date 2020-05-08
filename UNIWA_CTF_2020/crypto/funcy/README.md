# Funcy Crypto challenge

First of all, we can see that the challenge is written in `python2.7`. So, i'm gonna use `python2.7` in order to solve it, but doing it in `python3` is just fine. 
We see that there is a `flag` var with a `dummy` value, and a **fake** key. Then there is loop that encrypts each character of the **real** flag with. It takes the character, convert it to `hex`, then convert it to `integer` and `XORS`	the character with the `real` key. After that, the whole `encrypted`message is converted to `base64`. The final result is: `NjAzOTMyNjI0MDE4NDc2MDM5NDI1NDYxMzM5MzYxNTQ0MjMzOTMzNzM3MjA=`.  

Now let's reverse it. We need to:
* Decode the final string  
* `Bruteforce` all printable characters as possible `key`. Don't forget, that we need to convert every 2 bytes from `hex` to `integer`.
* Convert them to `integer` to `ascii`. 

A simple `python2.7` script I made.

```python
import base64

s1 = 'NjAzOTMyNjI0MDE4NDc2MDM5NDI1NDYxMzM5MzYxNTQ0MjMzOTMzNzM3MjA='
s = base64.b64decode(s1)
flag = ''
temp = ''

for key in range(32,255):
    flag = ''
    for i in range(0, len(s), 2): # 2 bytes
        temp = int(s[i:i+2]) ^ key
        flag += chr(temp)
    if 'UNIWA' in flag:
        print flag
```
```sh
$ python dec.py 
UNIWA{FUNC_TH4T_CH4LL}
```
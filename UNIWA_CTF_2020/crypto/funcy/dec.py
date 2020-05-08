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

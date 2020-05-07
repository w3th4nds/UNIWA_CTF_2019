import base64

# flag format: UNIWA{FL4G}

flag = 'This should be the flag..'
enc = ''
temp = ''
key = 1 # This key is FAKE! Someone messed up with it.. Find the correct one..
final_flag = ''
for i in flag:
    enc = i.encode('hex')
    enc = int(enc, 16)
    enc ^= key
    final_flag += str(enc)
final_flag = base64.b64encode(final_flag)
print 'This is the flag but it is encrypted..\n'
print 'NjAzOTMyNjI0MDE4NDc2MDM5NDI1NDYxMzM5MzYxNTQ0MjMzOTMzNzM3MjA='


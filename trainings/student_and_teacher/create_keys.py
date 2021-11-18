from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

private_key = RSA.generate(4096)
with open('private.pem','w') as f:
    f.write(private_key.export_key().decode('utf-8'))

public_key = private_key.publickey()
with open('public.pem', 'w') as f:
    f.write(public_key.export_key().decode('utf-8'))



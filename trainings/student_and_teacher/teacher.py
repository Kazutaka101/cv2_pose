from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import argparse

parser = argparse.ArgumentParser(description='Decrypt traning report')
parser.add_argument('f',help='file name which you want decript')
args = parser.parse_args()
#鍵の読み込み
with open('private.pem', 'br') as f:
    private_pem = f.read()
    private_key = RSA.import_key(private_pem)
 
with open(args.f, 'br') as f:
    data = f.read()
# メッセージを復号
private_cipher = PKCS1_OAEP.new(private_key)
#message2 = private_cipher.decrypt(ciphertext).decode("utf-8")
message =  private_cipher.decrypt(data)
print(message)
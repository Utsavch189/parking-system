from cryptography.fernet import Fernet
from django.conf import settings

def encrypt(content:str)->str:
    try:
        with open(f'{settings.BASE_DIR}/encription.key','rb') as seckey:
            key=seckey.read()
        f = Fernet(key)
        cipher_content=f.encrypt(content.encode())
        return cipher_content.decode()
    except Exception as e:
        raise Exception(str(e))

def decrypt(content:str):
    try:
        with open(f'{settings.BASE_DIR}/encription.key','rb') as seckey:
            key=seckey.read()
        f = Fernet(key)
        d=f.decrypt(content.encode())
        return d.decode()
    except Exception as e:
        print(e)
        raise Exception(str(e))

if __name__=="__main__":
    t="hello"
    enc=encrypt(t)
    print(enc)
    dec=decrypt(enc)
    print(dec)
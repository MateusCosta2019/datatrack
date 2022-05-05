import code
from time import time
from unicodedata import name
import pyotp
import os 
import time 
def gen_key():
    return pyotp.random_base32()

def gen_url(key):
    return pyotp.hotp.HOTP('JBSWY3DPEHPK3PXP').provisioning_uri(name="teste.com", issuer_name="Secure App", initial_count=0)

def generate_code(key):
    totp=pyotp.TOTP(key)
    return totp.now()

def verify_code(key, code):
    totp = pyotp.TOTP(key)
    totp.verify(code)
    
key = gen_key()
print(key)
uri = gen_url(key)
print(uri)

code = generate_code(key)
print (code)
time.sleep(120)
code2 = generate_code(key)

print(verify_code(key, code))
print(verify_code(key, code2))


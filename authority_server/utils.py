from config import JWT_PRIVKEY
import jwt

def gen_token(data):
    return jwt.encode(data, JWT_PRIVKEY, algorithm="EdDSA")

# TODO: implement this
def gen_decrypt_key():
    return ""

# TODO: implement this
def gen_encrypt_key():
    return ""
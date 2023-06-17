import os

with open("./ed25519key.pem", "r") as f:
    JWT_PRIVKEY = f.read()


with open("./password_hmac_key.txt", "r") as f:
    PASSWORD_HMAC_KEY = f.read()  # for password hashing

COOKIE_KEY = os.urandom(32)

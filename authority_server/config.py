with open('ed25519key.pem', 'rb') as f:
    JWT_PRIVKEY = f.read()
PASSWORD_HMAC_KEY = "secret_one" # for password hashing
COOKIE_KEY = "aaaa" # for password hashing
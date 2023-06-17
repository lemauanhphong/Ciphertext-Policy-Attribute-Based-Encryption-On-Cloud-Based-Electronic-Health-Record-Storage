with open("/run/secrets/jwt_key", "r") as f:
    JWT_PRIVKEY = f.read()

with open("/run/secrets/password_hmac_key", "r") as f:
    PASSWORD_HMAC_KEY = f.read()  # for password hashing

with open("/run/secrets/cookie_key", "r") as f:
    COOKIE_KEY = f.read()  # for password hashing

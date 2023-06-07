from functools import wraps
import jwt
from flask import request

with open("ec25519pubkey.pem", "rb") as f:
    pubkey = f.read()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            user = jwt.decode(token, pubkey, algorithms=["EdDSA"])
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
            }, 500

        return f(user, *args, **kwargs)

    return decorated
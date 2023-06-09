from functools import wraps
import jwt
from flask import request
from config import JWT_PUBKEY

check_role = lambda user_roles, accepted_roles: any(role in accepted_roles for role in user_roles)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")
            
        if not token or len(token) != 2:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        token = token[1]
        try:
            user = jwt.decode(token, JWT_PUBKEY, algorithms=["EdDSA"])
            user['check_role'] = check_role
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
            }, 500

        return f(user, *args, **kwargs)

    return decorated
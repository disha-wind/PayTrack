import hashlib
from datetime import timedelta, datetime, UTC

import bcrypt
import jwt
from sanic import Unauthorized


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_access_token(data: dict, secret_key, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm="HS256")

def verify_token(token: str, secret_key: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")

def generate_signature(data: dict, secret_key: str) -> str:
    sorted_keys = sorted(data.keys())
    concatenated = ''.join(str(data[key]) for key in sorted_keys)
    concatenated += secret_key
    return hashlib.sha256(concatenated.encode()).hexdigest()


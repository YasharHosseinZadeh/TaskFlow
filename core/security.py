import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

password_hash = PasswordHash.recommended()

def hash_password(password:str) -> str:
    return password_hash.hash(password)


def verify_password(password:str, hashed_password:str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id:int):
    expire = datetime.now(UTC) + timedelta(minutes=30)
    payload = {
        "sub": str(user_id),
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


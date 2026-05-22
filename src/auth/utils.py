from passlib.context import CryptContext
from src.config import Config
from datetime import datetime, timedelta
import jwt
import logging
import uuid
from passlib.hash import bcrypt

# passwd_context = CryptContext(
#     schemes=['bcrypt']
# )

# def generate_password_hash(password: str) -> str:
#     print("password is.........",password)
#     print(len(password))
#     # hash = passwd_context.hash(password)
#     hash = bcrypt.using(rounds=13).hash("password")
#     return hash

# def verify_password(password: str, hash: str) -> bool:
#     # return passwd_context.verify(password, hash)
#     return bcrypt.verify(password, hash)

# Create password hashing context
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Hash password
def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



... #the password functions
def create_access_token(user_data: dict , expiry:timedelta =None, refresh: bool= False) -> str:
    payload = {
        'user':user_data,
        'exp': datetime.now() + (expiry if expiry is not None else timedelta(minutes=60)),
        'jti': str(uuid.uuid4()),
        'refresh' : refresh
    }


    token = jwt.encode(
        payload=payload,
        key= Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWTError as jwte:
        logging.exception(jwte)
        return None

    except Exception as e:
        logging.exception(e)
        return None
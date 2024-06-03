import uuid
from datetime import timedelta
from typing import Dict

import jwt
import bcrypt
from fastapi import HTTPException, status

from app.settings.config_app import settings


def check_passwords_match(password: str, confirm_password: str):
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password and confirm password are different."
        )


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def check_password(password: str, hashed_password: bytes):
    if not bcrypt.checkpw(password.encode(), hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wrong password, try again."
        )


def create_access_token(email: str) -> str:
    to_encode = {
        "email": email,
        "exp": settings.TIME_MOSCOW_NOW + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4())
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(email: str) -> str:
    to_encode = {
        "email": email,
        "exp": settings.TIME_MOSCOW_NOW + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "jti": str(uuid.uuid4()),
        "refresh_token": True
    }
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, str]:
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if not decoded.get("refresh_token"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token"
            )
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token"
        )

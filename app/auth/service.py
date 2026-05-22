from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash

from ..config import settings

from pwdlib.hashers.bcrypt import BcryptHasher

pwd_hash = PasswordHash([BcryptHasher()])


def hash_password(password: str) -> str:
    return pwd_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_hash.verify(plain, hashed)


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> str:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    return payload["sub"]

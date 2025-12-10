from passlib.context import CryptContext
from fastapi_app.core.config import settings

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__time_cost=3,
    argon2__type="ID",
)

PEPPER = settings.security.password_pepper


def hash_password(password: str) -> str:
    return pwd_context.hash(password + PEPPER)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password + PEPPER, hashed_password)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def get_hash(input: str) -> str:
    return pwd_context.hash(input)


def verify_hash(input: str, hashed: str) -> bool:
    return pwd_context.verify(input, hashed)

import jwt
from dataclasses import dataclass
from passlib.context import CryptContext


@dataclass
class PasswordHash:
    SECRET_KEY = "some_secret_key"
    ALGORITHM = "HS256"
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.PWD_CONTEXT.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        return jwt.encode(data, self.SECRET_KEY, self.ALGORITHM)

    def decode_access_token(self, token: str) -> str:
        return jwt.decode(token, self.SECRET_KEY, self.ALGORITHM)



password_hash = PasswordHash()

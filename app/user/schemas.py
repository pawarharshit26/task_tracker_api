from pydantic import EmailStr
from app.core.schemas import BaseSchema


class SignupInputSchema(BaseSchema):
    name: str
    email: EmailStr
    password: str


class LoginInputSchema(BaseSchema):
    email: EmailStr
    password: str


class LoginOutputSchema(BaseSchema):
    id: int
    name: str
    email: EmailStr
    token: str

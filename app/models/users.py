from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=5, max_length=25)
    password_: str = Field(...)
    email: EmailStr


from pydantic import BaseModel


class LoginSchema(BaseModel):
    username: str
    password: str


class RefreshSchema(BaseModel):
    refresh: str


class VerifySchema(BaseModel):
    token: str


class TokenSchema(BaseModel):
    access: str
    refresh: str


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_superuser: bool
    is_staff: bool
    is_active: bool
    date_joined: str

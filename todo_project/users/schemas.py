from pydantic import BaseModel, Field, validator, EmailStr
from todo_project.users.schema_validations import (
    username_validation,
    password_validation,
)


class UserRegistrationRequest(BaseModel):
    """
    Pydentic models documentation link.
    https://pydantic-docs.helpmanual.io/usage/models/
    """
    username: str = Field(min_length=6, max_length=50, )
    first_name: str = Field(min_length=1, max_length=50, )
    last_name: str = Field(min_length=1, max_length=50, )
    hashed_password: str
    email: EmailStr

    # validators
    _username_validator = validator('username', allow_reuse=True)(username_validation)
    _password_validator = validator('hashed_password', allow_reuse=True)(password_validation)

    class Config:
        extra = "forbid"


class UserRegistrationResponse(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserLoginRequest(BaseModel):
    user_name: str = Field(min_length=6, max_length=50, )
    password: str

    # validators
    _username_validator = validator('user_name', allow_reuse=True)(username_validation)
    _password_validator = validator('password', allow_reuse=True)(password_validation)

    class Config:
        extra = "forbid"


class Token(BaseModel):
    access_token: str
    refresh_token: str


class PasswordChangeSchema(BaseModel):
    current_password: str
    new_password: str
    confirm_new_password: str

    # validators
    _password_validator = validator('new_password', allow_reuse=True)(password_validation)

    class Config:
        extra = "forbid"


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ForgotPasswordSetSchema(BaseModel):
    reset_token: str
    new_password: str
    confirm_new_password: str

    # validators
    _password_validator = validator('new_password', allow_reuse=True)(password_validation)

    class Config:
        extra = "forbid"

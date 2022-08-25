from typing import Any, Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Indexed, Document
from fastapi.encoders import jsonable_encoder
from pydantic import Field, EmailStr


class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: Indexed(str, unique=True)
    email: Indexed(EmailStr, unique=True)
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.now)

    def __repr__(self):
        return f"< User {self.user_id}>"

    @classmethod
    async def get_user(cls, username):
        try:
            user = await cls.find_one(cls.username == username)
            return user
        except:
            return None


    @classmethod
    async def check_is_username_exists(cls, username):
        try:
            user = await cls.find_one(cls.username == username)
            return user
        except:
            return None

    @classmethod
    async def check_is_email_exists(cls, email):
        try:
            user = await cls.find_one(cls.email == email)
            return user
        except:
            return None

    @classmethod
    async def save_user(cls, data):
        user = cls(**jsonable_encoder(data))
        await user.create()
        return user

    @classmethod
    async def update_password(cls, current_user, password):
        try:
            user = await cls.find_one(cls.username == current_user)
            user.password = password
            await user.save()
            return user
        except:
            return None

    @classmethod
    def get_user_emails(cls):
        return True

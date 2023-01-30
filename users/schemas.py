from pydantic import BaseModel, Field
from typing import Optional


class UserRegisterSchema(BaseModel):
    username: str
    phone: str
    password: str


class UserLoginSchema(BaseModel):
    phone: str
    password: str
    username: Optional[str]


class UserEditSchema(BaseModel):
    username: Optional[str]
    password_hash: Optional[str]
    userinfo: Optional[str]


class Chat(BaseModel):
    chat_name: str

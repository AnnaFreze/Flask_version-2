from typing import Optional, Type

import pydantic
from pydantic import BaseModel


class BaseUser(BaseModel):
    name: Optional[str]
    # password: Optional[str]

    # @pydantic.field_validator("password")
    # @classmethod
    # def secure_password(cls, value):
    #     if len(value) < 8:
    #         raise ValueError("password is too short")
    #     return value


class CreateUser(BaseUser):

    name: str
    # password: str


class UpdateUser(BaseUser):

    name: Optional[str]
    # password: Optional[str]

Schema_user = Type[CreateUser] | Type[UpdateUser]

class BaseAdv(BaseModel):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]

class CreateAdv(BaseAdv):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]

class UpdateAdv(BaseAdv):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]

Schema_adv = Type[CreateUser] | Type[UpdateUser]

class RelUser(BaseModel):
    adv: list["BaseAdv"]

class RelAdv(BaseModel):
    user: "BaseUser"


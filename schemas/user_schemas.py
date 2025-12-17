from pydantic import BaseModel
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str
    name: str
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None
    is_approver: Optional[bool] = None

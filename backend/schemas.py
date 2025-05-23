from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class BilletCreate(BaseModel):
    type: Literal['solo', 'duo', 'famille']
    client_name: str
    email: EmailStr

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BilletCreate(BaseModel):
    event: str
    date: datetime
    place: str
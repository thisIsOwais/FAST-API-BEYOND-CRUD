from pydantic import BaseModel, Field
import uuid 
from datetime import datetime
from src.books.model import BookModel as Book
from typing import List, Optional


class UserCreateModel(BaseModel):
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    email: str = Field(max_length=40)
    password: str  = Field(min_length=4,max_length=100)

class UserRegisterModel(BaseModel):
    uid: uuid.UUID
    first_name: str =Field(max_length=25)
    last_name:  str =Field(max_length=25)
    username: str = Field(max_length=8)
    role: str
    is_verified: bool 
    email: str = Field(max_length=40)
    password_hash: str  = Field(min_length=4, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)  


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str  = Field(min_length=4, max_length=100)

class UserBooksModel(UserRegisterModel):
    books: List["Book"]

class EmailModel(BaseModel):
    addresses : List[str]
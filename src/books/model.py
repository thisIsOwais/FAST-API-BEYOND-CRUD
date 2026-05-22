from pydantic import BaseModel
import uuid
from datetime import datetime   
class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: datetime
    page_count: int
    language: str
    uid: uuid.UUID
    created_at: datetime 
    updated_at: datetime 

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

class BookCreateModel(BaseModel):
    """
        This class is used to validate the request when creating or updating a book
    """
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
from typing import List

from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime
from sqlalchemy import func

# from src.books.schema import Book

from src.books.schema import Book


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )

    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    username: str = Field(min_length=2, max_length=14, unique=True)
    
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    ) 
    is_verified: bool = False
    email: str
    password_hash: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now()))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=func.now(), onupdate=func.now()))

    books: List["Book"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )


    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
    # def func():
    #     from src.books.schema import Book
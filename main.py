from fastapi import FastAPI, Header , status
from typing import Optional
from pydantic import BaseModel
from db import books
from fastapi.exceptions import HTTPException
from typing import List
from db import books


app = FastAPI()

@app.get('/')
async def read_root():
    return {"message": "Hello World!"}

#PATH PARAMETER
#inside main.py
@app.get('/greet/{username}')
async def greet(username:str):
   return {"message":f"Hello {username}"}

#QUERY PARAMETER
# inside main.py

user_list = [
   "Jerry",
   "Joey",
   "Phil"
]

users=[]

@app.get('/search')
async def search_for_user(username:str):
   for user in user_list:
    if username in user_list :
        return {"message":f"details for user {username}"}

    else:
        return {"message":"User Not Found"}
    


#OPTIONAL QUERY PARAMETER
@app.get('/greet/')
async def greet_optional(username:Optional[str]="User"):
   return {"message":f"Hello {username}"}


#REQUEST BODY
# inside main.py

# the User model
class UserSchema(BaseModel):
   username:str
   email:str


@app.post("/create_user")
async def create_user(user_data:UserSchema):
   new_user = {
      "username" : user_data.username,
      "email": user_data.email
   }

   users.append(new_user)

   return {"message":"User Created successfully","user":new_user}


# inside main.py
@app.get('/get_headers')
async def get_all_request_headers(
    user_agent: Optional[str] = Header(None),
    accept_encoding: Optional[str] = Header(None),
    referer: Optional[str] = Header(None),
    connection: Optional[str] = Header(None),
    accept_language: Optional[str] = Header(None),
    host: Optional[str] = Header(None),
):
    request_headers = {}
    request_headers["User-Agent"] = user_agent
    request_headers["Accept-Encoding"] = accept_encoding
    request_headers["Referer"] = referer
    request_headers["Accept-Language"] = accept_language
    request_headers["Connection"] = connection
    request_headers["Host"] = host

    return request_headers


#CRUD OPERATIONS OVER TEMPORARY BOOKS DATA

# the Book model
class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# BOOK UPDATE MODEL    
class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str


#Read all books
@app.get("/books", response_model=List[Book])
async def get_all_books():
    return books


#create a book
@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data: Book) -> dict:
    new_book = book_data.model_dump()

    books.append(new_book)

    return new_book

#get book by id
@app.get("/book/{book_id}")
async def get_book(book_id: int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# update book by id
@app.patch("/book/{book_id}")
async def update_book(book_id: int,book_update_data:BookUpdateModel) -> dict:

    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


#delete book by id
@app.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
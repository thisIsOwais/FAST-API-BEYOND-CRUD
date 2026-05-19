# from fastapi import APIRouter
# from src.books.book_data import books
# from src.books.model import BookSchema as Book, BookUpdateSchema as BookUpdateModel
# from typing import List
# from fastapi import HTTPException, status

# book_router = APIRouter()

# @book_router.get("/books", response_model=List[Book])
# async def get_all_books():
#     return books


# @book_router.post("/books", status_code=status.HTTP_201_CREATED)
# async def create_a_book(book_data: Book) -> dict:
#     new_book = book_data.model_dump()

#     books.append(new_book)

#     return new_book


# @book_router.get("/book/{book_id}")
# async def get_book(book_id: int) -> dict:
#     for book in books:
#         if book["id"] == book_id:
#             return book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


# @book_router.patch("/book/{book_id}")
# async def update_book(book_id: int,book_update_data:BookUpdateModel) -> dict:

#     for book in books:
#         if book['id'] == book_id:
#             book['title'] = book_update_data.title
#             book['publisher'] = book_update_data.publisher
#             book['page_count'] = book_update_data.page_count
#             book['language'] = book_update_data.language

#             return book

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


# @book_router.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             books.remove(book)

#             return {}

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.books.model import BookModel as Book, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.db.main import get_session
from typing import List


book_router = APIRouter()
book_service = BookService()


@book_router.get("/", response_model=List[Book])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_a_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
) -> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book


@book_router.get("/{book_uid}", response_model=Book)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    else:
        return updated_book


@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:

        return {}
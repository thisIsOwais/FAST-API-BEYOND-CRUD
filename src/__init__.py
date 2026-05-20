from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import user_router
from contextlib import asynccontextmanager
from src.db.main import initdb

#the lifespan event
@asynccontextmanager
async def lifespan(app: FastAPI):    
    print("Server is starting...")
    await initdb()  # Initialize the database when the server starts
    yield
    print("server is stopping")



version = "1.0.0"

app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version= version,
    lifespan=lifespan
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(user_router, prefix=f"/api/{version}/auth", tags=['auth'])
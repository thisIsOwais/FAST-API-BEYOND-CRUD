from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from src.tags.routes import tags_router
from contextlib import asynccontextmanager
from src.db.main import initdb
from .errors import register_error_handlers

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

register_error_handlers(app)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=['books'])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=['auth'])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"])
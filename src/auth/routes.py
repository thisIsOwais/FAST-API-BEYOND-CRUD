from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.auth.model import UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import List
from .service import UserService


user_router = APIRouter()
user_service = UserService()


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserLoginModel)
async def register_user(session: AsyncSession = Depends(get_session)):
    user= await user_service.create_user(session)
    return user



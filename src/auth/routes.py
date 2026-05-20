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

@user_router.get("/email/{email}", response_model=UserLoginModel)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@user_router.get("/exists/{email}")
async def check_user_exists(email: str, session: AsyncSession = Depends(get_session)):      
    exists = await user_service.user_exists(email, session)
    return {"exists": exists}   

from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.auth.model import UserLoginModel, UserRegisterModel, UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.utils import create_access_token, verify_password
from src.db.main import get_session
from typing import List
from .service import UserService


auth_router = APIRouter()
user_service = UserService()


@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserRegisterModel)
async def register_user(user_data: UserCreateModel , session: AsyncSession = Depends(get_session)):
    user= await user_service.create_user(user_data,session)
    print("user is.........",user)
    return user

@auth_router.get("/email/{email}", response_model=UserRegisterModel)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@auth_router.get("/exists/{email}")
async def check_user_exists(email: str, session: AsyncSession = Depends(get_session)):      
    exists = await user_service.user_exists(email, session)
    return {"exists": exists}   


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid)},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )


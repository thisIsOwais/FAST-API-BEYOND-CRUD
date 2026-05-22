from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from src.auth.model import UserLoginModel, UserRegisterModel, UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.utils import create_access_token, verify_password
from src.db.main import get_session
from typing import List
from .service import UserService
from datetime import timedelta, datetime
from src.auth.dependencies import AccessTokenBearer,RefreshTokenBearer,RoleChecker,get_current_user
from src.db.redis import add_jti_to_blocklist


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin"])


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
                expiry=timedelta(days=7),
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

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    print("token details in logout route is.........",token_details)
    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.get("/me", response_model=UserRegisterModel, dependencies=[Depends(role_checker)])
async def get_current_user(user=Depends(get_current_user), _: bool = Depends(role_checker)):
    print("current user in me route is.........",user)

    return user
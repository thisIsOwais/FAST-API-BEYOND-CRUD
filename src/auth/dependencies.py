# from typing import Any, Dict, Optional

# from fastapi import HTTPException, Request, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# def decode_token(token: str) -> Optional[Dict[str, Any]]:
#     """Placeholder token decoder. Replace with real implementation."""
#     if token and token != "":
#         # return dummy payload for valid-looking tokens
#         return {"sub": "user_id", "token": token}
#     return None


# class AccessTokenBearer(HTTPBearer):
#     def __init__(self, auto_error: bool = True):
#         super().__init__(auto_error=auto_error)

#     async def __call__(self, request: Request) -> Optional[Dict[str, Any]]:
#         creds: HTTPAuthorizationCredentials = await super().__call__(request)
#         token = creds.credentials if creds else None

#         token_data = decode_token(token) if token else None

#         if token_data is None:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail={
#                     "error": "This token is invalid or expired",
#                     "resolution": "Please get new token",
#                 },
#             )

#         return token_data

#     def token_valid(self, token: str) -> bool:
#         return decode_token(token) is not None

from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from typing import Any, List
from .schema import User
from src.errors import (
    InvalidToken,
    RefreshTokenRequired, 
    AccessTokenRequired, 
    InsufficientPermission
)


user_service = UserService()
class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
     
        token = creds.credentials

        token_data = decode_token(token)

        print("token data is........",token_data)
  

        if await token_in_blocklist(token_data['jti']):
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN, detail={
            #         "error":"This token is invalid or has been revoked",
            #         "resolution":"Please get new token"
            #     }
            # )
            raise InvalidToken()

        if not self.token_valid(token):
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN, detail={
            #         "error":"This token is invalid or expired",
            #         "resolution":"Please get new token"
            #     }
            # )
            raise InvalidToken()

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None 

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
       
        if token_data and token_data["refresh"]:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Please provide an access token",
        #     )
            raise AccessTokenRequired()


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            # raise HTTPException(
            #     status_code=status.HTTP_403_FORBIDDEN,
            #     detail="Please provide a refresh token",
            # )
            raise RefreshTokenRequired()
        
 
 
async def get_current_user(
     token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if current_user.role in self.allowed_roles:
            print(f"User role {current_user.role} is allowed to access this resource.")
            print(f"User role {self.allowed_roles} are allowed to access this resource.")
            return True

        # raise HTTPException(
        #     status_code = status.HTTP_403_FORBIDDEN,
        #     detail="You are not allowed to perform this action."
        # )
        raise InsufficientPermission()
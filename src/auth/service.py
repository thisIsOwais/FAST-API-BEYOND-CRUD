from .schema import User
from .model import UserCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .utils import generate_password_hash, verify_password
from src.db.main import get_session


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession):
        statement = select(User).where(User.email == email)

        result = await session.exec(statement)

        user = result.first()
        print("queried user is.........",user)
        return user

    async def user_exists(self, email, session: AsyncSession):
        user = await self.get_user_by_email(email, session)

        return True if user is not None else False

    async def create_user(self, user_data: UserCreateModel, session: AsyncSession):
        user_data_dict = user_data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(user_data_dict["password"])

        session.add(new_user)
        print("new user is.........",new_user)

        await session.commit()

        print("new user after commit is.........",new_user)
        return new_user
    

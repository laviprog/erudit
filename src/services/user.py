from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from src.database.models import User
from src.database.repositories.user import UserRepository
from src.services import Service


class UserService(Service[User]):
    def __init__(self, session: AsyncSession):
        repository = UserRepository(session)
        super().__init__(repository)
        self.repository: UserRepository = repository

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        user = await self.repository.get_by_telegram_id(telegram_id)
        return user

    async def create(self, telegram_id: int, **kwargs) -> User:
        existing_user = await self.repository.get_by_telegram_id(telegram_id)

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        user = User(telegram_id=telegram_id, **kwargs)
        return await self.repository.add(user)
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Application
from src.database.repositories.application import ApplicationRepository
from src.services import Service


class ApplicationService(Service[Application]):
    def __init__(self, session: AsyncSession):
        repository = ApplicationRepository(session)
        super().__init__(repository)
        self.repository: ApplicationRepository = repository

    async def get_all_by_telegram_id(self, telegram_id: int) -> List[Application]:
        return await self.repository.get_all_by_telegram_id(telegram_id)

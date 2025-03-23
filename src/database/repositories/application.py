from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.models import Application, Event, User
from src.database.repositories import Repository


class ApplicationRepository(Repository[Application]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Application)

    async def get_all_by_telegram_id(self, telegram_id: int) -> List[Application]:
        result = await self.session.execute(
            select(Application)
            .join(User)
            .join(Event)
            .filter(User.telegram_id == telegram_id)
            .filter(Event.event_time > func.now())
            .options(selectinload(Application.event))
        )

        return list(result.scalars().all())

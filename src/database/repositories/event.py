from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Event
from src.database.repositories import Repository


class EventRepository(Repository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Event)

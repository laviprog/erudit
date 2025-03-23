from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Event
from src.database.repositories.event import EventRepository
from src.services import Service


class EventService(Service[Event]):
    def __init__(self, session: AsyncSession):
        repository = EventRepository(session)
        super().__init__(repository)
        self.repository: EventRepository = repository
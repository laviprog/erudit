from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Application
from src.database.repositories import Repository


class ApplicationRepository(Repository[Application]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Application)

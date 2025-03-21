from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Admin
from src.database.repositories import Repository


class AdminRepository(Repository[Admin]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Admin)

import logging

from typing import Generic, TypeVar, Optional, List

from src.database.models import Base
from src.database.repositories import Repository

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Base)


class Service(Generic[T]):
    def __init__(self, repository: Repository[T]):
        self.repository = repository

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        return await self.repository.get_by_id(obj_id)

    async def get_all(self) -> List[T]:
        return await self.repository.get_all()

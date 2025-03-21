from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Generic, Type, TypeVar, Optional, List

from src.database.models import Base

T = TypeVar("T", bound=Base)

class Repository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def add(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        result = await self.session.execute(select(self.model).filter(self.model.id == obj_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> List[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def delete(self, obj_id: int) -> None:
        obj = await self.get_by_id(obj_id)

        if obj:
            await self.session.delete(obj)
            await self.session.commit()

    async def update(self, obj: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(obj, key, value)

        await self.session.commit()
        return obj
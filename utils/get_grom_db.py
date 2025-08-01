from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from db.settings import get_db, async_session_maker


async def get_settings_string():
    async with async_session_maker() as session:  # Используем async_session_maker напрямую
        query = select(models.SettingsStrings).filter_by(id=1)
        result = await session.execute(query)
        settings_string = result.scalars().first()
        return settings_string
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session


class DependsMixin:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

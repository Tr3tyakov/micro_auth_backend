from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class ImageModel(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

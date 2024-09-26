from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import UUIDType

from app.database import Base


class DocumentDataModel(Base):
    __tablename__ = "docs"

    id = Column(UUIDType(binary=False), nullable=False, primary_key=True)
    body = Column(String(255), nullable=True)
    effective_count = Column(Integer, default=0)

from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DocumentBase(BaseModel):
    body: Optional[str] = None
    effective_count: Optional[int] = None


class DocumentCreate(DocumentBase):
    document_id: UUID


class DocumentUpdate(DocumentBase):
    pass

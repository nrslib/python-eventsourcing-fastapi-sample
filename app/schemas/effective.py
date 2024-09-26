from uuid import UUID

from pydantic.main import BaseModel


class EffectivePost(BaseModel):
    doc_id: UUID
    user_id: UUID


class EffectiveDelete(BaseModel):
    doc_id: UUID
    user_id: UUID

from uuid import UUID

from app.database import SessionLocal
from app.module.pubsubdoc.infrastructure.doc.crud import get_document_by_id
from app.module.pubsubdoc.infrastructure.doc.models import DocumentDataModel


class DocumentQueryService:
    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_document(self, doc_id: UUID) -> DocumentDataModel:
        """指定されたIDのドキュメントを取得します。"""
        document = get_document_by_id(self.db, doc_id)
        return document

    def get_all_documents(self):
        """全ドキュメントを取得します。"""
        docs = self.db.query(DocumentDataModel).all()
        return docs

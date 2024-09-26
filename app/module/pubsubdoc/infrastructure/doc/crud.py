from uuid import UUID

from sqlalchemy.orm import Session

from app.module.pubsubdoc.infrastructure.doc.models import DocumentDataModel
from app.module.pubsubdoc.infrastructure.doc.schema import DocumentUpdate, DocumentCreate


def create_document(db: Session, document: DocumentCreate) -> DocumentDataModel:
    db_document = DocumentDataModel(id=document.document_id, body=document.body, effective_count=document.effective_count)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return document


def get_document_by_id(db: Session, document_id: UUID) -> DocumentDataModel:
    return db.query(DocumentDataModel).filter(DocumentDataModel.id == document_id).first()


def update_document(db: Session, document_id: UUID, document: DocumentUpdate):
    db_document = db.query(DocumentDataModel).filter(DocumentDataModel.id == document_id).first()
    if not db_document:
        return None

    # リクエストで送られたフィールドのみ更新する
    for var, value in vars(document).items():
        if value is not None:
            setattr(db_document, var, value)

    db.commit()
    db.refresh(db_document)
    return db_document

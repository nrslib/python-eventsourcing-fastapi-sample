from contextlib import contextmanager

from eventsourcing.dispatch import singledispatchmethod
from eventsourcing.system import ProcessApplication

from app.database import SessionLocal
from app.module.pubsubdoc.domain.models.doc import Doc
from app.module.pubsubdoc.domain.models.effective import Effective
from app.module.pubsubdoc.infrastructure.doc.crud import create_document, get_document_by_id, update_document
from app.module.pubsubdoc.infrastructure.doc.schema import DocumentCreate, DocumentUpdate


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DocumentDataModelProjection(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(Doc.DocCreated)
    def handle(self, event: Doc.DocCreated, process_event):
        document_create = DocumentCreate(document_id=event.originator_id, body=event.body, effective_count=0)
        with get_db() as db:
            create_document(db, document_create)

    @policy.register(Doc.DocModified)
    def handle(self, event: Doc.DocModified, process_event):
        document_update = DocumentUpdate(body=event.body)
        with get_db() as db:
            update_document(db, event.originator_id, document_update)

    @policy.register(Effective.EffectiveCreated)
    def handle(self, event: Effective.EffectiveCreated, _):
        with get_db() as db:
            document = get_document_by_id(db, event.doc_id)
            update_document(db, event.doc_id, DocumentUpdate(effective_count=document.effective_count + 1))

    @policy.register(Effective.EffectiveMarked)
    def handle(self, event: Effective.EffectiveMarked, _):
        with get_db() as db:
            document = get_document_by_id(db, event.doc_id)
            update_document(db, event.doc_id, DocumentUpdate(effective_count=document.effective_count + 1))

    @policy.register(Effective.EffectiveUnmarked)
    def handle(self, event: Effective.EffectiveUnmarked, _):
        with get_db() as db:
            document = get_document_by_id(db, event.doc_id)
            update_document(db, event.doc_id, DocumentUpdate(effective_count=document.effective_count - 1))

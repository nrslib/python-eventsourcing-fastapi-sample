from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.services import get_doc_service, get_document_query_service
from app.module.pubsubdoc.application.query.document.document_query_service import DocumentQueryService
from app.module.pubsubdoc.application.services.doc_service import DocService
from app.schemas.docs import DocsPost, DocsPut

router = APIRouter()


@router.post("/documents/")
def post_docs(request: DocsPost, doc_service: DocService = Depends(get_doc_service)):
    doc_id = doc_service.create(request.contents)

    return doc_id


@router.get("/documents/{doc_id}")
def get(doc_id: UUID, document_query_service: DocumentQueryService = Depends(get_document_query_service)):
    document = document_query_service.get_document(doc_id)

    return document


@router.put("/documents/{doc_id}")
def put(doc_id: UUID, request: DocsPut, doc_service: DocService = Depends(get_doc_service)):
    doc_service.modify(doc_id, request.contents)

    return doc_id

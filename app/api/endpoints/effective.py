from fastapi import APIRouter
from fastapi.params import Depends

from app.core.services import get_effective_service, effective_service
from app.module.pubsubdoc.application.services.effective_service import EffectiveService
from app.schemas.effective import EffectivePost, EffectiveDelete

router = APIRouter()


@router.post("/effective/")
def post_effective(request: EffectivePost, effective_service: EffectiveService = Depends(get_effective_service)):
    effective_id = effective_service.mark(request.doc_id, request.user_id)

    return effective_id


@router.delete("/effective/")
def delete(request: EffectiveDelete):
    effective_service.unmark(request.doc_id, request.user_id)

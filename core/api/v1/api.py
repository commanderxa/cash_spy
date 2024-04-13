from fastapi import APIRouter

from ..v1.auth import router as auth_router
from ..v1.card import router as card_router
from ..v1.banks import router as bank_router
from ..v1.offer import router as offer_router


router = APIRouter(prefix="/v1", tags=["monitor"])

router.include_router(auth_router, prefix="/auth")
router.include_router(card_router, prefix="/cards")
router.include_router(bank_router, prefix="/banks")
router.include_router(offer_router, prefix="/offers")

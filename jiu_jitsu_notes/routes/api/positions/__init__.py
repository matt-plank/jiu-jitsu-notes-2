from fastapi import APIRouter

from . import editable, static

router = APIRouter()
router.include_router(editable.router)
router.include_router(static.router)

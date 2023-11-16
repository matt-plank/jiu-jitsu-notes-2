from fastapi import APIRouter

from . import editable, page, static

router = APIRouter()
router.include_router(page.router)
router.include_router(static.router)
router.include_router(editable.router)

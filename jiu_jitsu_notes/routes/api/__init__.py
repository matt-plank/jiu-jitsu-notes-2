from fastapi import APIRouter

from . import auth, groups, positions, techniques

router = APIRouter()
router.include_router(groups.router, prefix="/groups")
router.include_router(positions.router)
router.include_router(techniques.router, prefix="/positions")
router.include_router(auth.router, prefix="/auth")

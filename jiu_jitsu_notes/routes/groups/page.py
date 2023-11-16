from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def groups_page(request: Request, db: Session = Depends(get_db)):
    groups = db.query(PositionGroup).all()

    return templates.TemplateResponse(
        "pages/all_groups.html",
        {
            "request": request,
            "groups": groups,
        },
    )


@router.get("/{group_id}")
async def get_group(
    request: Request,
    group_id: int,
    db: Session = Depends(get_db),
):
    group: PositionGroup | None = db.query(PositionGroup).filter_by(id=group_id).first()

    if group is None:
        raise HTTPException(
            status_code=404,
            detail=f"No group with id {group_id!r}",
        )

    return templates.TemplateResponse(
        "pages/group.html",
        {
            "request": request,
            "group": group,
        },
    )

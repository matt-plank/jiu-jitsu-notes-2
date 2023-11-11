from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..models import PositionGroup

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_all_groups(request: Request, db: Session = Depends(get_db)):
    groups = db.query(PositionGroup).all()

    return templates.TemplateResponse(
        "pages/all_groups.html",
        {
            "request": request,
            "groups": groups,
        },
    )


@router.get("/{group_name}")
async def get_group(request: Request, group_name: str, db: Session = Depends(get_db)):
    group: PositionGroup | None = db.query(PositionGroup).filter_by(name=group_name).first()

    if group is None:
        raise HTTPException(
            status_code=404,
            detail=f"No group called {group_name!r}",
        )

    return templates.TemplateResponse(
        "pages/position_group.html",
        {
            "request": request,
            "group": group,
            "format": "title",
        },
    )


@router.post("/")
async def create_group(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    group = schemas.NewGroup(**form_data)  # type: ignore
    db_group = PositionGroup(**group.model_dump())

    db.add(db_group)
    db.commit()

    return templates.TemplateResponse(
        "components/group/static.html",
        {
            "request": request,
            "group": db_group,
        },
    )


@router.post("/edit")
async def create_group_editable(request: Request):
    return templates.TemplateResponse(
        "components/group/new.html",
        {
            "request": request,
        },
    )

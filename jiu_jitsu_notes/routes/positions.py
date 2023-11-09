from fastapi import Depends, HTTPException
from fastapi.requests import Request
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Position
from ..schemas import NewPosition, PartialPosition

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{position_id}")
async def get_position(request: Request, position_id: int, db: Session = Depends(get_db)):
    position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    return templates.TemplateResponse(
        "components/position/static.html",
        {
            "request": request,
            "position": position,
        },
    )


@router.put("/{position_id}")
async def update_position(
    request: Request,
    position_id: int,
    db: Session = Depends(get_db),
):
    db_position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if db_position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    form_data = await request.form()
    position = PartialPosition(**form_data)  # type: ignore

    if position.name is not None:
        db_position.name = position.name

    if position.description is not None:
        db_position.description = position.description

    db.commit()

    return templates.TemplateResponse(
        "components/position/static.html",
        {
            "request": request,
            "position": db_position,
        },
    )


@router.post("/")
async def create_position(
    request: Request,
    db: Session = Depends(get_db),
):
    form_data = await request.form()
    position = NewPosition(**form_data)  # type: ignore
    db_position = Position(**position.model_dump())

    group_id_str: str | None = request.query_params.get("groupId")

    if group_id_str is not None:
        group_id = int(group_id_str)
        db_position.group_id = group_id

    db.add(db_position)
    db.commit()

    return templates.TemplateResponse(
        "components/position/static.html",
        {
            "request": request,
            "position": position,
        },
    )


@router.get("/{position_id}/edit")
async def get_editable(request: Request, position_id: int, db: Session = Depends(get_db)):
    position: Position | None = db.query(Position).filter_by(id=position_id).first()

    if position is None:
        raise HTTPException(
            status_code=404,
            detail=f"No position with id {position_id!r}",
        )

    return templates.TemplateResponse(
        "components/position/editable.html",
        {
            "request": request,
            "position": position,
        },
    )


@router.post("/edit")
async def new_editable(request: Request):
    return templates.TemplateResponse(
        "components/position/new.html",
        {
            "request": request,
            "group_id": request.query_params.get("groupId"),
        },
    )

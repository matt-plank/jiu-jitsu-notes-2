from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .. import schemas
from ..db import get_db
from ..models import Position, Technique

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/{technique_id}")
async def get_single_technique(
    request: Request,
    technique_id: int,
    db: Session = Depends(get_db),
):
    technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    return templates.TemplateResponse(
        "components/technique/static.html",
        {
            "request": request,
            "technique": technique,
        },
    )


@router.put("/{technique_id}")
async def update_single_technique(
    request: Request,
    technique_id: int,
    db: Session = Depends(get_db),
):
    form_data = await request.form()
    technique = schemas.PartialTechnique(**form_data)  # type: ignore
    db_technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

    if db_technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    if technique.name is not None:
        db_technique.name = technique.name

    if technique.description is not None:
        db_technique.description = technique.description

    if technique.to_position_id is not None:
        db_technique.to_position_id = technique.to_position_id

    db.commit()

    return templates.TemplateResponse(
        "components/technique/static.html",
        {
            "request": request,
            "technique": db_technique,
        },
    )


@router.post("/")
async def create_technique(
    request: Request,
    fromPositionId: int,
    toPositionId: int,
    db: Session = Depends(get_db),
):
    form_data = await request.form()
    technique = schemas.NewTechnique(**form_data)  # type: ignore
    db_technique = Technique(
        **technique.model_dump(),
        from_position_id=fromPositionId,
        to_position_id=toPositionId,
    )

    db.add(db_technique)
    db.commit()

    return templates.TemplateResponse(
        "components/technique/static.html",
        {
            "request": request,
            "technique": db_technique,
        },
    )


@router.get("/{technique_id}/editable")
async def get_editable_for_position(
    request: Request,
    technique_id: int,
    db: Session = Depends(get_db),
):
    technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique found with id {technique_id!r}",
        )

    return templates.TemplateResponse(
        "components/technique/editable.html",
        {
            "request": request,
            "technique": technique,
            "positions": db.query(Position).all(),
        },
    )


@router.post("/editable")
async def create_editable(
    request: Request,
    fromPositionId: int,
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        "components/technique/new.html",
        {
            "request": request,
            "from_position_id": fromPositionId,
            "positions": db.query(Position).all(),
        },
    )

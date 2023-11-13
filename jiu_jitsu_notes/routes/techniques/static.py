from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ... import schemas
from ...db import get_db
from ...models import Technique

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


@router.get("/{technique_id}/detailed")
async def get_detailed_technique(
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
        "components/technique/detailed.html",
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
    db: Session = Depends(get_db),
):
    form_data = await request.form()

    technique = schemas.NewTechnique(
        **form_data,  # type: ignore
        from_position_id=fromPositionId,
    )

    db_technique = Technique(**technique.model_dump())

    db.add(db_technique)
    db.commit()

    return templates.TemplateResponse(
        "components/technique/static.html",
        {
            "request": request,
            "technique": db_technique,
        },
    )


@router.delete("/{technique_id}")
async def delete_technique(request: Request, technique_id: int, db: Session = Depends(get_db)):
    technique: Technique | None = db.query(Technique).filter_by(id=technique_id).first()

    if technique is None:
        raise HTTPException(
            status_code=404,
            detail=f"No technique with id {technique_id!r}",
        )

    db.delete(technique)
    db.commit()

    return PlainTextResponse(content="")

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "pages/login.html",
        {
            "request": request,
        },
    )


@router.post("/")
async def login(request: Request):
    """Assume the user is logged in, redirect to the index page."""
    return RedirectResponse(url="/")

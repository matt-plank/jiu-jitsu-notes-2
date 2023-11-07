from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .db import engine
from .models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def get(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )

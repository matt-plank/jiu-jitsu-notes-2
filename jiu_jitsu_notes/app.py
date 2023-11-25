from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import engine
from .models import Base
from .routes import api, pages

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")

app.mount("/css", StaticFiles(directory="templates/css"), name="static")

templates = Jinja2Templates(directory="templates")

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .db import engine
from .models import Base
from .routes import groups, positions

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(groups.router, prefix="/groups")
app.include_router(positions.router, prefix="/positions")

templates = Jinja2Templates(directory="templates")

from fastapi import FastAPI
from fastapi.requests import Request

app = FastAPI()


@app.get("/")
def get(request: Request):
    return {"message": "Hello, World!"}

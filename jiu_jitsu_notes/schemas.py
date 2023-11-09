from pydantic import BaseModel, Field


class NewPosition(BaseModel):
    name: str
    description: str


class PartialPosition(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)


class NewGroup(BaseModel):
    name: str
    description: str

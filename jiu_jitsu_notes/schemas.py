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


class NewTechnique(BaseModel):
    name: str
    description: str


class PartialTechnique(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    to_position_id: int | None = Field(None)

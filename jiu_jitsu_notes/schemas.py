from pydantic import BaseModel, Field


class PartialPosition(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)

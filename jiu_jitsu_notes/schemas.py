from pydantic import BaseModel, Field, validator


class NewPosition(BaseModel):
    name: str
    description: str


class PartialPosition(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)


class NewGroup(BaseModel):
    name: str
    description: str


class PartialGroup(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)


class NewTechnique(BaseModel):
    name: str
    description: str
    from_position_id: int
    to_position_id: int | None = Field(None)

    @validator("to_position_id", pre=True)
    def empty_string_to_none(cls, id):
        if id == "":
            return None

        return id


class PartialTechnique(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    to_position_id: int | None = Field(None)

    @validator("to_position_id", pre=True)
    def empty_string_to_none(cls, id):
        if id == "":
            return None

        return id

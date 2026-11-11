from pydantic import BaseModel, ConfigDict


class MaterialResponse(BaseModel):
    id: int
    title: str
    type: str
    author: str | None
    source: str | None
    url: str | None

    model_config = ConfigDict(from_attributes=True)


class MaterialCreate(BaseModel):
    title: str
    type: str
    author: str | None = None
    source: str | None = None
    url: str | None = None
    user_id: int
    topic_id: int

class MaterialUpdate(BaseModel):
    title: str | None = None
    type: str | None = None
    author: str | None = None
    source: str | None = None
    url: str | None = None

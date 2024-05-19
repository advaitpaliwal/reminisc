from pydantic import BaseModel


class MemoryQuery(BaseModel):
    query: str
    user_id: str


class MemoryBase(BaseModel):
    content: str = None


class MemoryCreate(MemoryBase):
    user_id: str


class MemoryResponse(MemoryBase):
    metadata: dict = {}

    class Config:
        from_attributes = True

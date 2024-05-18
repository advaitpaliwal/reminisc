from pydantic import BaseModel


class MemoryQuery(BaseModel):
    query: str


class MemoryBase(BaseModel):
    content: str = None


class MemoryCreate(MemoryBase):
    pass


class MemoryResponse(MemoryBase):
    metadata: dict = {}

    class Config:
        from_attributes = True

import traceback
from fastapi import APIRouter, Depends, HTTPException
from reminisc.api.schemas.memory import MemoryCreate, MemoryResponse, MemoryQuery
from reminisc.api.services.memory import MemoryService

router = APIRouter(
    prefix="/memory",
    tags=["memory"],
)


@router.post("/", response_model=MemoryResponse)
async def create_memory(data: MemoryCreate, service: MemoryService = Depends()):
    try:
        created_memory = service.create_memory(data.content, data.user_id)
        return created_memory
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[MemoryResponse])
async def get_memories(user_id: str, service: MemoryService = Depends()):
    try:
        memories = service.get_all_memories(user_id)
        return memories
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str, service: MemoryService = Depends()):
    try:
        service.delete_memory(memory_id)
        return {"message": "Memory deleted successfully"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=list[MemoryResponse])
async def search_memories(data: MemoryQuery, service: MemoryService = Depends()):
    try:
        relevant_memories = service.search_memories(data.query, data.user_id)
        return relevant_memories
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/classify")
async def classify_input(data: MemoryQuery, service: MemoryService = Depends()):
    try:
        should_store_memory = service.classify_input(
            data.query, data.user_id)
        return {"should_store_memory": should_store_memory}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process", response_model=MemoryResponse)
async def process_user_input(data: MemoryQuery, service: MemoryService = Depends()):
    try:
        memory = service.process_user_input(data.query, data.user_id)
        return memory
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

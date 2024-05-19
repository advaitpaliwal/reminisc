from fastapi import Depends
from reminisc.api.schemas.memory import MemoryResponse
from reminisc.src.memory.manager import MemoryManager


class MemoryService:
    def __init__(self, manager: MemoryManager = Depends()):
        self.manager = manager

    def create_memory(self, memory: str, user_id: str) -> MemoryResponse:
        created_memory = self.manager.add_memory(memory, user_id)
        return MemoryResponse(**created_memory)

    def get_all_memories(self, user_id: str) -> list[MemoryResponse]:
        memories = self.manager.load_all_memories(user_id)
        return [MemoryResponse(**memory) for memory in memories]

    def delete_memory(self, memory_id: str):
        self.manager.remove_memory(memory_id)

    def search_memories(self, query: str, user_id: str) -> list[MemoryResponse]:
        memories = self.manager.search_memory(query, user_id)
        return [MemoryResponse(content=memory.page_content, metadata=memory.metadata) for memory in memories]

    def classify_input(self, user_input: str, user_id: str) -> bool:
        return self.manager.classify(user_input, user_id)

    def process_user_input(self, user_input: str, user_id: str) -> MemoryResponse | None:
        memory = self.manager.handle_user_input(user_input, user_id)
        if memory:
            return MemoryResponse(**memory)
        return MemoryResponse()

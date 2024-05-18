from fastapi import Depends
from reminisc.api.schemas.memory import MemoryResponse
from reminisc.src.memory.manager import MemoryManager


class MemoryService:
    def __init__(self, manager: MemoryManager = Depends()):
        self.manager = manager

    def create_memory(self, memory: str) -> MemoryResponse:
        created_memory = self.manager.add_memory(memory)
        return MemoryResponse(**created_memory)

    def get_all_memories(self) -> list[MemoryResponse]:
        memories = self.manager.load_all_memories()
        return [MemoryResponse(**memory) for memory in memories]

    def delete_memory(self, memory_id: str):
        self.manager.remove_memory(memory_id)

    def search_memories(self, query: str) -> list[MemoryResponse]:
        memories = self.manager.search_memory(query)
        return [MemoryResponse(content=memory.page_content, metadata=memory.metadata) for memory in memories]

    def classify_input(self, user_input: str) -> bool:
        return self.manager.classifier.classify(user_input)

    def process_user_input(self, user_input: str) -> MemoryResponse | None:
        memory = self.manager.handle_user_input(user_input)
        if memory:
            return MemoryResponse(**memory)
        return MemoryResponse()

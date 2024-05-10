from reminisc.src.vectordb import VectorDB
from reminisc.src.memory.creator import MemoryCreator
import logging

logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self):
        self.vectordb = VectorDB()
        self.memory_creator = MemoryCreator()
        logger.info("MemoryManager initialized")

    def store_memory(self, user_input: str):
        memory = self.memory_creator.create_memory(user_input)
        logger.info(f"Memory created: {memory}")
        self.vectordb.add(memory)

    def retrieve_memory(self, query: str):
        results = self.vectordb.search(query)
        return results

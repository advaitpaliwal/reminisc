from reminisc.src.vectordb import VectorDB
import logging

logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self):
        self.vectordb = VectorDB()
        logger.info("MemoryManager initialized")

    def store_memory(self, memory: str):
        self.vectordb.add(memory)

    def retrieve_memory(self, query: str):
        results = self.vectordb.search(query)
        memory = ""
        for doc in results:
            memory += doc.page_content + "\n"
        return memory

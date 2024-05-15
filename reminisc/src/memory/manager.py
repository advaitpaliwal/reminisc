import json
from reminisc.src.vectordb import VectorDB
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self, memory_file="memories.json"):
        self.vectordb = VectorDB()
        self.memory_file = memory_file
        self.load_memories()
        logger.info("MemoryManager initialized")

    def store_memory(self, memory: str):
        memory_id = self.vectordb.add(memory)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        memory_entry = {
            "id": memory_id,
            "timestamp": timestamp,
            "memory": memory
        }
        self.memories.append(memory_entry)
        self.save_memories()

    def retrieve_memory(self, query: str):
        results = self.vectordb.search(query)
        memory = ""
        for doc in results:
            memory += doc.page_content + "\n"
        return memory

    def load_memories(self):
        if os.path.exists(f"local/{self.memory_file}"):
            with open(f"local/{self.memory_file}", "r") as file:
                self.memories = json.load(file)
        else:
            self.memories = []

    def save_memories(self):
        with open(f"local/{self.memory_file}", "w") as file:
            json.dump(self.memories, file, indent=4)

    def delete_memory(self, memory_id: str):
        self.memories = [
            memory for memory in self.memories if memory["id"] != memory_id]
        self.save_memories()
        self.vectordb.delete(memory_id)

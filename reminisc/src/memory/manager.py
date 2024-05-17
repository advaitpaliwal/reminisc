import os
import logging
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings

load_dotenv()
logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self):
        self.table_name = "documents"
        self.embedder = OpenAIEmbeddings()
        self.client = self._init_supabase_client()
        self.vectordb = self._init_vectordb()
        self.memories = self.load_memories()
        logger.info("MemoryManager initialized")

    def _init_supabase_client(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        return create_client(url, key)

    def _init_vectordb(self):
        return SupabaseVectorStore(
            embedding=self.embedder,
            client=self.client,
            table_name=self.table_name,
            query_name="match_documents",
        )

    def store_memory(self, memory: str):
        metadata = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.vectordb.add_texts(texts=[memory], metadatas=[metadata])
        logger.info(f"Stored memory: {memory}")

    def retrieve_memory(self, query: str):
        results = self.vectordb.similarity_search(query)
        memory = ""
        for doc in results:
            memory += doc.page_content + "\n"
        return memory

    def load_memories(self):
        result = self.client.table(self.table_name).select(
            "id, content, metadata->timestamp").execute()
        logger.info(f"Loaded memories: {result}")
        return result.data

    def delete_memory(self, memory_id: str):
        self.vectordb.delete(ids=[memory_id])
        logger.info(f"Deleted memory: {memory_id}")


if __name__ == "__main__":
    manager = MemoryManager()
    print(manager.load_memories())

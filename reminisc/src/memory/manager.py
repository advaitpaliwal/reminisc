import os
import logging
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from reminisc.src.memory.classifier import MemoryClassifier
from reminisc.src.memory.creator import MemoryCreator
from uuid import uuid4

load_dotenv()
logger = logging.getLogger(__name__)


class MemoryManager:
    def __init__(self):
        self.documents_table = "documents"
        self.classifications_table = "classifications"
        self.embedder = OpenAIEmbeddings()
        self.classifier = MemoryClassifier()
        self.creator = MemoryCreator()
        self.client = self._initialize_supabase_client()
        self.vectordb = self._initialize_vector_db()
        self.memories = self.load_all_memories()
        logger.info("MemoryManager initialized")

    def _initialize_supabase_client(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        return create_client(url, key)

    def _initialize_vector_db(self):
        return SupabaseVectorStore(
            embedding=self.embedder,
            client=self.client,
            table_name=self.documents_table,
            query_name="match_documents",
        )

    def add_memory(self, memory: str):
        memory_id = str(uuid4())
        metadata = {
            "id": memory_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.vectordb.add_texts(texts=[memory], metadatas=[
                                metadata], ids=[memory_id])
        logger.info(f"Memory added: {memory}")
        return metadata | {"content": memory}

    def search_memory(self, query: str):
        results = self.vectordb.similarity_search(query)
        logger.info(f"Search results: {results}")
        return results

    def load_all_memories(self):
        result = self.client.table(self.documents_table).select(
            "id, content, metadata"
        ).execute()
        logger.info(f"Loaded memories: {result}")
        return result.data

    def create_memory(self, user_input: str):
        memory = self.creator.create_memory(user_input)
        memory_data = self.add_memory(memory)
        return memory_data

    def remove_memory(self, memory_id: str):
        self.vectordb.delete(ids=[memory_id])
        logger.info(f"Memory removed: {memory_id}")

    def classify(self, user_input: str) -> bool:
        classification = self.classifier.classify(user_input)
        self.save_classification(user_input, classification)
        return classification

    def save_classification(self, user_input: str, classification: bool):
        classification_id = str(uuid4())
        data = {
            "id": classification_id,
            "input": user_input,
            "classification": classification,
            "model": self.classifier.model_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.client.table(self.classifications_table).insert(data).execute()
        logger.info(f"Classification saved: {data}")

    def handle_user_input(self, user_input: str) -> dict | None:
        logger.info(f"User Input: {user_input}")
        should_store_memory = self.classify(user_input)
        logger.info(f"Should store memory: {should_store_memory}")
        if should_store_memory:
            logger.info("Storing memory")
            memory_data = self.create_memory(user_input)
            logger.info(f"Memory created: {memory_data}")
            return memory_data
        else:
            return None

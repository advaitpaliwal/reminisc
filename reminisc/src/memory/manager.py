from openai import OpenAI
import os
import logging
from reminisc.config.config import Config
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
        self.memories_table = "memories"
        self.classifications_table = "classifications"
        self.client = self._initialize_supabase_client()
        self.vectordb = None
        logger.info("MemoryManager initialized")

    def _initialize_supabase_client(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        return create_client(url, key)

    def _initialize_vector_db(self, openai_api_key):
        # Initialize embedder with API key
        self.embedder = OpenAIEmbeddings(api_key=openai_api_key)
        return SupabaseVectorStore(
            embedding=self.embedder,
            client=self.client,
            table_name=self.memories_table,
            query_name="match_memories",
        )

    def add_memory(self, memory: str, user_id: str, openai_api_key: str):
        if not self.vectordb:
            self.vectordb = self._initialize_vector_db(openai_api_key)
        memory_id = str(uuid4())
        metadata = {
            "id": memory_id,
            "user_id": user_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.vectordb.add_texts(texts=[memory], metadatas=[
                                metadata], ids=[memory_id])
        logger.info(f"Memory added: {memory} for user {user_id}")
        return metadata | {"content": memory}

    def search_memory(self, query: str, user_id: str, openai_api_key: str):
        if not self.vectordb:
            self.vectordb = self._initialize_vector_db(openai_api_key)
        results = self.vectordb.similarity_search(
            query, filter={"user_id": user_id})
        logger.info(f"Search results: {results} for user {user_id}")
        return results

    def load_all_memories(self, user_id: str):
        result = self.client.table(self.memories_table).select(
            "id, content, metadata").eq("metadata->>user_id", user_id).execute()
        logger.info(f"Loaded memories: {result} for user {user_id}")
        return result.data

    def create_memory(self, user_input: str, user_id: str, openai_api_key: str):
        self.creator = MemoryCreator(
            openai_api_key=openai_api_key)
        memory = self.creator.create_memory(user_input)
        memory_data = self.add_memory(memory, user_id, openai_api_key)
        return memory_data

    def remove_memory(self, memory_id: str, openai_api_key: str):
        if not self.vectordb:
            self.vectordb = self._initialize_vector_db(openai_api_key)
        self.vectordb.delete(ids=[memory_id])
        logger.info(f"Memory removed: {memory_id}")

    def classify(self, user_input: str, user_id: str, openai_api_key: str):
        self.classifier = MemoryClassifier(
            openai_api_key=openai_api_key)
        classification = self.classifier.classify(user_input)
        self.save_classification(user_input, classification, user_id)
        return classification

    def save_classification(self, user_input: str, classification: bool, user_id: str):
        classification_id = str(uuid4())
        data = {
            "id": classification_id,
            "user_id": user_id,
            "input": user_input,
            "classification": classification,
            "model": self.classifier.model_name,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.client.table(self.classifications_table).insert(data).execute()
        logger.info(f"Classification saved: {data}")

    def handle_user_input(self, user_input: str, user_id: str, openai_api_key: str) -> dict | None:
        logger.info(f"User Input: {user_input}")
        should_store_memory = self.classify(
            user_input, user_id, openai_api_key)
        logger.info(f"Should store memory: {should_store_memory}")
        if should_store_memory:
            logger.info("Storing memory")
            memory_data = self.create_memory(
                user_input, user_id, openai_api_key)
            logger.info(f"Memory created: {memory_data}")
            return memory_data
        else:
            return None

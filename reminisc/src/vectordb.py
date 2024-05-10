import os
import logging
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec


load_dotenv()
logger = logging.getLogger(__name__)


class VectorDB:
    def __init__(self):
        self.client = Pinecone()
        self.index_name = os.getenv("PINECONE_INDEX_NAME")
        self.embedder = OpenAIEmbeddings()
        self.vectordb = self._init_vectordb()
        logger.info("VectorDB initialized")

    def _init_vectordb(self):
        if self.index_name not in self.client.list_indexes().names():
            self.client.create_index(
                name=self.index_name,
                metric="cosine",
                dimension=1536,  # dimensionality of text-embedding-ada-002
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            logger.info(f"Created VectorDB index: {self.index_name}")
        return PineconeVectorStore.from_existing_index(
            index_name=self.index_name, embedding=self.embedder
        )

    def add(self, memory: str):
        self.vectordb.add_texts([memory])
        logger.info(f"Added memory to VectorDB: {memory}")

    def search(self, query: str):
        results = self.vectordb.similarity_search(query)
        logger.info(f"Searched VectorDB for query: {query}")
        logger.info(f"Search results: {results}")
        return results

    def delete(self, memory_ids: list):
        self.vectordb.delete(ids=memory_ids)
        logger.info(f"Deleted memories from VectorDB: {memory_ids}")


if __name__ == "__main__":
    vectordb = VectorDB()

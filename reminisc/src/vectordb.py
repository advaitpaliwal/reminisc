import os
import logging
from dotenv import load_dotenv
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings

load_dotenv()
logger = logging.getLogger(__name__)


class VectorDB:
    def __init__(self):
        self.index_name = os.getenv("CHROMA_INDEX_NAME")
        self.embedder = OpenAIEmbeddings()
        self.vectordb = self._init_vectordb()
        logger.info("VectorDB initialized")

    def _init_vectordb(self):
        return Chroma(
            collection_name=self.index_name,
            embedding_function=self.embedder,
            persist_directory="./local/vectorstore",
        )

    def add(self, memory: str) -> str:
        ids = self.vectordb.add_texts([memory])
        logger.info(f"Added memory to VectorDB: {memory}")
        return ids[0]

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

# agents/job_agents/rag_store.py
import logging
from typing import List, Dict
from pathlib import Path
import os
import faiss

from llama_index.core import (VectorStoreIndex, Document, StorageContext, Settings)
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

logger = logging.getLogger(__name__)

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

class JobMarketRAGStore:
    def __init__(self, llm):
        Settings.llm = llm
        self.vector_store_dir = Path("data/vector_store")
        self.vector_store_dir.mkdir(parents=True, exist_ok=True)
        self.persist_path = str(self.vector_store_dir)
        self.index = self._load_or_create_index()

    def _load_or_create_index(self):
        embedding_dimension = 384
        if os.path.exists(os.path.join(self.persist_path, "docstore.json")):
            logger.info("Loading existing vector store from disk...")
            vector_store = FaissVectorStore.from_persist_dir(self.persist_path)
            storage_context = StorageContext.from_defaults(vector_store=vector_store, persist_dir=self.persist_path)
            return VectorStoreIndex.from_documents([], storage_context=storage_context)
        else:
            logger.info("Creating new vector store...")
            faiss_index = faiss.IndexFlatL2(embedding_dimension)
            vector_store = FaissVectorStore(faiss_index=faiss_index)
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            return VectorStoreIndex.from_documents([], storage_context=storage_context)

    def add_jobs(self, jobs: List[Dict]):
        documents = []
        for job in jobs:
            text = f"Title: {job.get('title', '')}\nCompany: {job.get('company_name', '')}\nLocation: {job.get('location', '')}\nDescription: {job.get('description', '')}"
            doc = Document(text=text, metadata={"title": job.get('title', ''), "company": job.get('company_name', '')})
            documents.append(doc)
        
        if not documents:
            logger.warning("No new documents to add to the RAG store.")
            return
        logger.info(f"Adding {len(documents)} new jobs to the vector store...")
        for doc in documents:
            self.index.insert(doc)
        
        self.index.storage_context.persist(persist_dir=self.persist_path)
        logger.info("Successfully saved updated vector store to disk.")

    def query(self, query_text: str) -> str:
        logger.info(f"Querying RAG store with: '{query_text}'")
        query_engine = self.index.as_query_engine()
        response = query_engine.query(query_text)
        return str(response)
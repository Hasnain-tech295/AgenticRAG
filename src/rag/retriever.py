# Vector/ hybrid search logic -> right now embedding in this file because we are using chromaDB 
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

filename = Path(".\knowledge_base")
class VectorStore:
    """Store and retrieve document embeddings"""
    def __init__(self, collection_name: str = "knowledge_base", persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        
        # Using openai embeddings
        openai_ef = embedding_functions.OpenAIEmbeddingFunction(
            api_key=os.getenv("OPENAI_API_KEY"),
            model_name="text-embedding-3-small"
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=openai_ef
        )
        
        print(f"✅ Vector store initialized: {collection_name}")
        print(f"   Documents: {self.collection.count()}")
        
    def add_chunks(self, chunks: List[Dict]):
        """Add document chunks to vector store"""
        if not chunks:
            print("No chunk found")
            return
        
        # Prepare data for chromaDB
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Add to collections (ChromaDB automatically generates embeddings)
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ Added {len(chunks)} chunks to vector store")
        
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Semantic search for relevant chunks"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        chunks = []
        
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                chunks.append({
                    "text": doc,
                    "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                    "distance": results['distances'][0][i] if results['distances'] else 0,
                    "id": results['ids'][0][i] if results['ids'] else f"chunk_{i}"
                })
        
        return chunks
    
    def clear(self):
        """Clear all documents from collection"""
        self.client.delete_collection(self.collection.name)
        print(f"🗑️  Cleared collection: {self.collection.name}")
from retriever import VectorStore
from index import DocumentChunker
from typing import List, Dict
from config.config import RagConfig

config = RagConfig()
class RAGPipeline:
    def __init__(self, config: RagConfig):
        self.chunker = DocumentChunker(
            chunk_size=config.chunk_size,
            overlap=config.chunk_overlap
        )
        
        self.vector_store = VectorStore(
            collection_name=config.collection_name
        )
        
        print("RAG Agent Initialized")
        
    def ingest_documents(self, documents: List[Dict]):
        """
        Ingest documents into the knowledge base
        
        Args:
            documents: List of dicts with 'content', 'source', 'title'
        """
        print(f"\n📥 Ingesting {len(documents)} documents...")
        
        # Chunk documents
        chunks = self.chunker.chunk_documents(documents)
        
        # Add to vector store
        self.vector_store.add_chunks(chunks)
        
        print("Documents ingested successfully")
        
    def retrieve(self, query: str, top_k: int) -> List[Dict]:
        """Retrieve relevant chunk for a query"""
        print(f"\n🔍 Searching for: '{query}'")
        
        chunks = self.vector_store.search(query, top_k=3)
        
        print(f"📚 Found {len(chunks)} relevant chunks")
        
        for i, chunk in enumerate(chunks, 1):
            print(f"  {i}. {chunk['metadata'].get('source', 'unknown')} (distance: {chunk.get('distance', 0):.3f})")
            
        return chunks
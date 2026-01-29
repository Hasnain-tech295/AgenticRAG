import tiktoken
from typing import Dict, Any, List
# Document chunking
class DocumentChunker:
    """Split documents into chunks for embeddings"""
    
    def __init__(self, chunk_size: int, overlap: int):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk_text(self, text: str, metadata: Dict[str, Any] = {}) -> List[Dict]:
        chunks = []
        text = text.strip()
        
        # Simple Character based chunking
        start = 0
        chunk_id = 0
        
        while start < len(text):
            # Get chunk
            end = start + self.chunk_size
            chunk_text = text[start : end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_sentence = max(
                    chunk_text.rfind('. '),
                    chunk_text.rfind('? '),
                    chunk_text.rfind('! ')
                )
                
                if last_sentence != -1:
                    chunk_text = chunk_text[:last_sentence + 1]
                    end = start + last_sentence + 1
            
            # create chunks with metadata
            chunks.append({
                "text": chunk_text.strip(),
                "chunk_id": chunk_id,
                "start_char": start,
                "end_char": end,
                "metadata": metadata or {}
            })
            
            # Move to next chunk with overlap
            start = end - self.overlap
            chunk_id += 1
        
        return chunks
    
    def chunk_documents(self, documents: List[Dict]) -> List[Dict]:
        """Chunk multiple documents"""
        all_chunks = []
        try: 
            for doc in documents:
                chunks = self.chunk_text(
                    text = doc.get("content", ""),
                    metadata={
                        "source": doc.get("source", "unknown"),
                        "title": doc.get("title", ""),
                        **doc.get("metadata", {})
                    }
                )
                
                all_chunks.extend(chunks)
        
            print(f"📄 Chunked {len(documents)} documents into {len(all_chunks)} chunks")
            return all_chunks
        
        except Exception as e:
            print(f"❌ Chunking failed: {e}")
            raise

    
    
    
"""
Knowledge Refresh Agent for AXIOMAI.

This agent handles re-indexing of documents in the vector database
when knowledge is detected as stale or causing hallucinations.
"""
from datetime import datetime
from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from app.core.config import settings


class KnowledgeRefreshAgent:
    """
    Agent responsible for refreshing knowledge in the vector database.
    
    Triggered when:
    - Hallucination is detected
    - Documents are stale
    
    Decides between partial re-index (1-2 docs) or full re-index (>2 docs).
    """
    
    PARTIAL_THRESHOLD = 2  # Documents affected threshold for partial vs full refresh
    
    def __init__(self):
        """Initialize embeddings and Pinecone connection."""
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX_NAME)
    
    def refresh(self, reason: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Refresh knowledge in the vector database.
        
        Args:
            reason: Why refresh is needed ("hallucination_detected", "stale_documents")
            documents: List of documents to re-index. Each document should have:
                       - "id": unique identifier
                       - "content": text content
                       - "metadata": optional metadata dict
        
        Returns:
            {
                "refresh_type": "partial" | "full",
                "updated_documents": int,
                "status": "completed"
            }
        """
        if not documents:
            self._log(reason, "none", 0)
            return {
                "refresh_type": "none",
                "updated_documents": 0,
                "status": "completed"
            }
        
        # Decide refresh type based on document count
        refresh_type = "partial" if len(documents) <= self.PARTIAL_THRESHOLD else "full"
        
        # Perform the appropriate refresh
        if refresh_type == "partial":
            updated_count = self._partial_reindex(documents)
        else:
            updated_count = self._full_reindex(documents)
        
        # Log the refresh activity
        self._log(reason, refresh_type, updated_count)
        
        return {
            "refresh_type": refresh_type,
            "updated_documents": updated_count,
            "status": "completed"
        }
    
    def _partial_reindex(self, documents: List[Dict[str, Any]]) -> int:
        """
        Re-embed and update only the affected documents.
        
        Args:
            documents: List of documents to re-index
            
        Returns:
            Number of documents updated
        """
        updated = 0
        for doc in documents:
            doc_id = doc.get("id")
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            if not doc_id or not content:
                continue
            
            # Generate new embedding
            embedding = self.embeddings.embed_query(content)
            
            # Upsert to Pinecone (update if exists, insert if new)
            self.index.upsert(
                vectors=[{
                    "id": doc_id,
                    "values": embedding,
                    "metadata": {**metadata, "content": content}
                }]
            )
            updated += 1
        
        return updated
    
    def _full_reindex(self, documents: List[Dict[str, Any]]) -> int:
        """
        Re-embed and rebuild all provided documents in the vector database.
        
        Args:
            documents: List of documents to re-index
            
        Returns:
            Number of documents updated
        """
        vectors_to_upsert = []
        
        for doc in documents:
            doc_id = doc.get("id")
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            if not doc_id or not content:
                continue
            
            # Generate new embedding
            embedding = self.embeddings.embed_query(content)
            
            vectors_to_upsert.append({
                "id": doc_id,
                "values": embedding,
                "metadata": {**metadata, "content": content}
            })
        
        # Batch upsert for efficiency
        if vectors_to_upsert:
            self.index.upsert(vectors=vectors_to_upsert)
        
        return len(vectors_to_upsert)
    
    def _log(self, reason: str, refresh_type: str, doc_count: int) -> None:
        """
        Log refresh activity for traceability.
        
        Args:
            reason: Why refresh was triggered
            refresh_type: "partial", "full", or "none"
            doc_count: Number of documents updated
        """
        timestamp = datetime.now().isoformat()
        log_entry = (
            f"[KNOWLEDGE REFRESH] "
            f"Timestamp: {timestamp} | "
            f"Reason: {reason} | "
            f"Type: {refresh_type} | "
            f"Documents Updated: {doc_count}"
        )
        print(log_entry)

from typing import List, Dict, Any
from datetime import datetime, timezone
import numpy as np
from sentence_transformers import SentenceTransformer, util
from app.core.config import settings

class AnswerValidatorAgent:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        # Weights
        self.W_SIMILARITY = 0.4
        self.W_SOURCE = 0.3
        self.W_FRESHNESS = 0.3
        self.TRUST_THRESHOLD = 0.65

    def validate(self, answer: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validates the generated answer against retrieved documents.
        Returns a dict with trust_score and decision.
        """
        if not documents:
             return {
                "trust_score": 0.0,
                "decision": "untrusted"
            }

        # 1. Similarity Score
        similarity_score = self._compute_similarity(answer, documents)
        
        # 2. Source Count Weight
        source_score = self._compute_source_weight(documents)
        
        # 3. Freshness Weight
        freshness_score = self._compute_freshness_weight(documents)
        
        # Final Trust Score
        trust_score = (
            (self.W_SIMILARITY * similarity_score) +
            (self.W_SOURCE * source_score) +
            (self.W_FRESHNESS * freshness_score)
        )
        
        # Round to 3 decimals for cleanliness
        trust_score = round(trust_score, 3)
        
        decision = "trusted" if trust_score >= self.TRUST_THRESHOLD else "untrusted"
        
        return {
            "trust_score": trust_score,
            "decision": decision,
            "components": {
                "similarity": round(similarity_score, 3),
                "source_score": round(source_score, 3),
                "freshness_score": round(freshness_score, 3)
            }
        }

    def _compute_similarity(self, answer: str, documents: List[Dict[str, Any]]) -> float:
        """
        Computes cosine similarity between answer and documents.
        Returns average similarity.
        """
        try:
            # Encode answer
            answer_emb = self.model.encode(answer, convert_to_tensor=True)
            
            # Encode documents
            doc_contents = [doc.get("content", "") for doc in documents]
            doc_embs = self.model.encode(doc_contents, convert_to_tensor=True)
            
            # Compute cosine similarities
            # util.cos_sim returns a matrix [num_query, num_corpus]
            # Here it is [1, num_docs]
            cosine_scores = util.cos_sim(answer_emb, doc_embs)
            
            # Take the mean of the scores
            # converting tensor to numpy float
            avg_similarity = cosine_scores.mean().item()
            
            # Ensure between 0 and 1
            return max(0.0, min(1.0, avg_similarity))
        except Exception as e:
            print(f"Error computing similarity: {e}")
            return 0.0

    def _compute_source_weight(self, documents: List[Dict[str, Any]]) -> float:
        """
        Computes score based on number of unique sources.
        """
        unique_ids = set()
        for doc in documents:
            metadata = doc.get("metadata", {})
            # Assuming 'doc_id' is the field for source identifier
            if "doc_id" in metadata:
                unique_ids.add(metadata["doc_id"])
            else:
                # If no doc_id, treat the whole doc as a unique unknown source? 
                # Or skip? Instructions say "Based on unique doc_id values".
                # If missing, we can't count it as a unique trusted source ID.
                # But let's check if content hash or something else is standard.
                # For now, stick to user spec "doc_id".
                pass
        
        count = len(unique_ids)
        
        if count >= 3:
            return 1.0
        elif count == 2:
            return 0.7
        else:
            return 0.4

    def _compute_freshness_weight(self, documents: List[Dict[str, Any]]) -> float:
        """
        Computes freshness score based on 'published_at'.
        """
        scores = []
        now = datetime.now(timezone.utc)
        
        for doc in documents:
            metadata = doc.get("metadata", {})
            pub_at_str = metadata.get("published_at")
            
            if not pub_at_str:
                scores.append(0.5)
                continue
                
            try:
                # Start by trying standard ISO format parsing
                # Adjust format if known, but isoformat is safest default assumption
                pub_date = datetime.fromisoformat(pub_at_str)
                
                # Verify timezone awareness
                if pub_date.tzinfo is None:
                    # Assume UTC if not specified, to compare with now(res)
                    pub_date = pub_date.replace(tzinfo=timezone.utc)
                
                delta = now - pub_date
                days = delta.days
                
                if days <= 30:
                    scores.append(1.0)
                elif days <= 180:
                    scores.append(0.7)
                else:
                    scores.append(0.4)
            except ValueError:
                # Fallback if date parsing fails
                scores.append(0.5)
                
        if not scores:
            return 0.5
            
        return sum(scores) / len(scores)

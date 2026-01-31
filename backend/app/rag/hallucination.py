from typing import List, Dict, Any
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.utils.math import cosine_similarity
from app.core.config import settings

class HallucinationDetectorAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
        # Threshold as per design philosophy (can be tuned)
        self.similarity_threshold = 0.76 

    def detect(self, answer: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Splits answer into claims and verifies each against retrieved documents.
        Returns dictionary with hallucination flag and list of unsupported claims.
        """
        # 1. Claim Extraction - Simple sentence splitting
        # Filter out empty strings
        claims = [c.strip() for c in answer.split('.') if c.strip()]
        
        if not claims:
            return {
                "hallucination": False,
                "unsupported_claims": []
            }

        # Extract text content from documents (handle both dict and object formats)
        doc_texts = []
        for doc in documents:
            if isinstance(doc, dict):
                doc_texts.append(doc.get('content', ''))
            else:
                doc_texts.append(doc.page_content)
        
        if not doc_texts:
            # If no documents retrieved, everything is technically unsupported/hallucination
            return {
                "hallucination": True,
                "unsupported_claims": claims
            }

        # 2. Claim Verification
        # Embed all documents once for efficiency
        doc_embeddings = self.embeddings.embed_documents(doc_texts)
        
        unsupported_claims = []
        is_hallucination = False

        for claim in claims:
            # Embed the single claim
            claim_embedding = self.embeddings.embed_query(claim)
            
            # Calculate cosine similarity between claim and ALL docs
            # result is [[score1, score2, ...]]
            scores = cosine_similarity([claim_embedding], doc_embeddings)[0]
            
            # 3. Decision Logic
            # Check if ANY document supports this claim with high similarity
            best_score = float(np.max(scores))
            
            if best_score < self.similarity_threshold:
                unsupported_claims.append(claim)
                is_hallucination = True
        
        return {
            "hallucination": is_hallucination,
            "unsupported_claims": unsupported_claims
        }

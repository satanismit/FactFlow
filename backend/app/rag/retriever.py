import os
from typing import List, Dict, Any

# Fix Windows OSError 1455 by disabling symlinks, safetensors aggressive usage, and limiting threads
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["SAFETENSORS_FAST_GPU"] = "0"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings

class RetrieverAgent:
    def __init__(self):
        # Fix for Windows OSError 1455 (Paging file too small): Force CPU and limit thread memory
        # We pass 'use_safetensors': False to force standard PyTorch weight loading instead of mmap
        # This bypasses the Windows paging file memory overload (OS Error 1455)
        model_kwargs = {
            'device': 'cpu',
            'trust_remote_code': True
        }
        encode_kwargs = {
            'normalize_embeddings': True
        }
        
        # Override the underlying transformer to force PyTorch binary loading
        os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = '0'
        
        # Force sentence-transformers to avoid safetensors if passing `model_kwargs` doesn't stick
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_NAME,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        # HuggingFace uses sentence-transformers beneath. 
        # Safetensors mmap is failing. We can try deleting the .safetensors file in the cache, or bypass it.
        self.vectorstore = PineconeVectorStore(
            index_name=settings.PINECONE_INDEX_NAME,
            embedding=self.embeddings,
            pinecone_api_key=settings.PINECONE_API_KEY
        )

    def retrieve(self, query: str) -> List[Dict[str, Any]]:
        cleaned_query = query.strip()
        if not cleaned_query:
            return []

        results = self.vectorstore.similarity_search_with_score(
            query=cleaned_query,
            k=settings.TOP_K
        )

        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "score": score
            })
        
        return formatted_results

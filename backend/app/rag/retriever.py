from typing import List, Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings

class RetrieverAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
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

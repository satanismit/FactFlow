import os
import sys

# Ensure backend directory is in path to import app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings

def ingest_data():
    print(f"Initializing embeddings: {settings.EMBEDDING_MODEL_NAME}")
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

    # Detailed FactFlow Knowledge Base
    documents = [
        {
            "text": "FactFlow is a production-oriented, agentic Retrieval-Augmented Generation (RAG) system focused on reliability, trust scoring, hallucination detection, and self-healing knowledge refresh.",
            "source": "FactFlow Architecture Overview"
        },
        {
            "text": "Core Design Philosophy of FactFlow: 1. Retrieval comes before generation (retrieval-first AI). 2. Every answer must be validated. 3. Low-trust answers must not silently pass. 4. Hallucinations must be detected and handled. 5. Knowledge must self-refresh when stale.",
            "source": "FactFlow Design Philosophy"
        },
        {
            "text": "FactFlow Query Preprocessor Agent: Cleans and normalizes user queries, detects intent, and prepares the query for retrieval.",
            "source": "Agent: Query Preprocessor"
        },
        {
            "text": "FactFlow Retriever Agent: Embeds the query using BGE-large, searches the Pinecone Vector Database, and returns Top-K document chunks with metadata. It performs no generation.",
            "source": "Agent: Retriever"
        },
        {
            "text": "FactFlow LLM Answer Generator Agent: Takes retrieved documents ONLY and generates a draft answer. It does not decide trust.",
            "source": "Agent: Generator"
        },
        {
            "text": "FactFlow Answer Validator Agent: Evaluates the generated answer using similarity between answer and documents, number of independent sources, and freshness of documents. Computes a Trust Score (0-1).",
            "source": "Agent: Validator"
        },
        {
            "text": "FactFlow Trust Score Logic: Trust Score = 0.4 * similarity_score + 0.3 * source_count_weight + 0.3 * freshness_weight. If score >= threshold (0.65), answer is trusted. Otherwise, untrusted.",
            "source": "Trust Score Logic"
        },
        {
            "text": "FactFlow Hallucination Detector Agent: Triggered when trust is low. Splits answer into atomic claims, verifies each claim against retrieved documents, and flags unsupported claims.",
            "source": "Agent: Hallucination Detector"
        },
        {
            "text": "FactFlow Knowledge Refresh Agent: Triggered when hallucination or stale knowledge is detected. Decides between partial or full re-index and updates the Vector DB.",
            "source": "Agent: Knowledge Refresh"
        }
    ]

    texts = [doc["text"] for doc in documents]
    metadatas = [{"source": doc["source"], "chunk_id": i} for i, doc in enumerate(documents)]

    print(f"Ingesting {len(texts)} documents into Pinecone index '{settings.PINECONE_INDEX_NAME}'...")
    
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=settings.PINECONE_API_KEY
    )

    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    
    print("✅ Sample data ingested successfully.")

if __name__ == "__main__":
    ingest_data()

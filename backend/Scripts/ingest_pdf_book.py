import os
import sys
from datetime import datetime

# Ensure backend directory is in path to import app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from app.core.config import settings

def ingest_pdf_book(pdf_path: str):
    """
    Ingest a PDF book into Pinecone vector database.
    
    Args:
        pdf_path: Path to the PDF file
    """
    print(f"Starting PDF ingestion: {pdf_path}")
    
    # 1. Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File not found at {pdf_path}")
        return
    
    # 2. Load PDF
    print("Loading PDF...")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF")
    
    # 3. Split into chunks
    print("Splitting into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Reasonable chunk size for technical content
        chunk_overlap=200,  # Overlap to maintain context
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    
    # 4. Initialize embeddings
    print(f"Initializing embeddings: {settings.EMBEDDING_MODEL_NAME}")
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
    
    # 5. Prepare metadata
    book_name = os.path.basename(pdf_path)
    timestamp = datetime.now().isoformat()
    
    # Add metadata to each chunk
    for i, chunk in enumerate(chunks):
        chunk.metadata.update({
            "source": book_name,
            "chunk_id": i,
            "total_chunks": len(chunks),
            "ingestion_date": timestamp,
            "doc_type": "book"
        })
    
    # 6. Ingest into Pinecone
    print(f"Ingesting into Pinecone index '{settings.PINECONE_INDEX_NAME}'...")
    
    vectorstore = PineconeVectorStore(
        index_name=settings.PINECONE_INDEX_NAME,
        embedding=embeddings,
        pinecone_api_key=settings.PINECONE_API_KEY
    )
    
    # Add documents in batches to avoid timeout
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        print(f"Ingesting batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}...")
        vectorstore.add_documents(batch)
    
    print(f"Successfully ingested {len(chunks)} chunks from {book_name}")
    print(f"Book: {book_name}")
    print(f"Total Pages: {len(documents)}")
    print(f"Total Chunks: {len(chunks)}")
    print(f"Index: {settings.PINECONE_INDEX_NAME}")

if __name__ == "__main__":
    # Path to the PDF book
    pdf_path = os.path.join(os.path.dirname(__file__), "..", "..", "booklet.pdf")
    pdf_path = os.path.abspath(pdf_path)
    
    print(f"PDF Path: {pdf_path}")
    ingest_pdf_book(pdf_path)

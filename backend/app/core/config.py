import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "BAAI/bge-large-en-v1.5")
    TOP_K = int(os.getenv("TOP_K", "5"))

settings = Config()

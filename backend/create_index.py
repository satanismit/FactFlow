import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("PINECONE_INDEX_NAME")

if not api_key:
    print("Error: PINECONE_API_KEY not found in .env")
    exit(1)

if not index_name:
    print("Error: PINECONE_INDEX_NAME not found in .env")
    exit(1)

print(f"Connecting to Pinecone with API key: {api_key[:5]}...")
pc = Pinecone(api_key=api_key)

existing_indexes = [index.name for index in pc.list_indexes()]

if index_name not in existing_indexes:
    print(f"Creating index: {index_name}")
    try:
        pc.create_index(
            name=index_name,
            dimension=384, # Dimension for BAAI/bge-small-en-v1.5
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print("Index created successfully. Waiting for it to accept connections...")
        time.sleep(10) # Wait a bit for initialization
    except Exception as e:
        print(f"Failed to create index: {e}")
        # Fallback for non-serverless or different region error handling if needed
else:
    print(f"Index '{index_name}' already exists.")

import os
import sys

# Ensure backend directory is in path to import app
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from pinecone import Pinecone
from app.core.config import settings

def clear_pinecone_index():
    """
    Deletes all vectors from the Pinecone index.
    """
    print(f"Connecting to Pinecone index: {settings.PINECONE_INDEX_NAME}")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    
    # Get index stats before deletion
    stats = index.describe_index_stats()
    total_vectors = stats.get('total_vector_count', 0)
    
    print(f"Current vector count: {total_vectors}")
    
    if total_vectors == 0:
        print("Index is already empty!")
        return
    
    # Confirm deletion
    print("\nWARNING: This will delete ALL vectors from the index!")
    confirm = input("Type 'yes' to confirm deletion: ")
    
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return
    
    print("\nDeleting all vectors...")
    
    # Delete all vectors by deleting all IDs
    # Use delete_all if supported, otherwise delete by namespace
    try:
        index.delete(delete_all=True)
        print("Successfully deleted all vectors!")
    except Exception as e:
        print(f"Error: {e}")
        print("Trying alternative deletion method...")
        
        # Alternative: Delete by namespace (if you're using namespaces)
        # Or fetch and delete in batches
        try:
            # Get all namespaces
            namespaces = stats.get('namespaces', {})
            if namespaces:
                for namespace in namespaces.keys():
                    print(f"Deleting namespace: {namespace}")
                    index.delete(delete_all=True, namespace=namespace)
            else:
                # Delete from default namespace
                index.delete(delete_all=True, namespace='')
            print("Successfully deleted all vectors!")
        except Exception as e2:
            print(f"Error with alternative method: {e2}")
    
    # Verify deletion
    stats_after = index.describe_index_stats()
    remaining = stats_after.get('total_vector_count', 0)
    print(f"\nVectors remaining: {remaining}")
    
    if remaining == 0:
        print("Index is now empty and ready for new data!")
    else:
        print(f"Warning: {remaining} vectors still remain.")

if __name__ == "__main__":
    clear_pinecone_index()

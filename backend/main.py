from app.rag.retriever import RetrieverAgent
import os

def main():
    print("Initializing Retriever Agent...")
    try:
        agent = RetrieverAgent()
        
        query = "What is the FactFlow system?"
        print(f"Query: {query}")
        
        results = agent.retrieve(query)
        
        print(f"\nRetrieved {len(results)} chunks:")
        for i, res in enumerate(results):
            print(f"\nChunk {i+1}:")
            print(f"Score: {res['score']:.4f}")
            print(f"Content: {res['content'][:200]}...") # Truncate for display
            print(f"Metadata: {res['metadata']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

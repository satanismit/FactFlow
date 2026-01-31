from app.rag.retriever import RetrieverAgent
from app.rag.hallucination import HallucinationDetectorAgent
import os

def main():
    print("Initializing Agents...")
    try:
        retriever = RetrieverAgent()
        detector = HallucinationDetectorAgent()
        
        query = "What is the FactFlow system?"
        print(f"\n--- 1. Retrieval ---")
        print(f"Query: {query}")
        
        results = retriever.retrieve(query)
        print(f"Retrieved {len(results)} chunks.")

        # Test Case 1: Supported Answer
        print(f"\n--- 2. Hallucination Detection (Test Case: SAFE) ---")
        safe_answer = "FactFlow is an agentic RAG system. It uses a retrieval-first architecture."
        print(f"Answer: {safe_answer}")
        
        safe_result = detector.detect(safe_answer, results)
        print(f"Result: {safe_result}")

        # Test Case 2: Hallucinated Answer
        print(f"\n--- 3. Hallucination Detection (Test Case: HALLUCINATION) ---")
        hallucinated_answer = "FactFlow uses a graph database called Neo4j as its primary storage."
        print(f"Answer: {hallucinated_answer}")
        
        hallucinated_result = detector.detect(hallucinated_answer, results)
        print(f"Result: {hallucinated_result}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

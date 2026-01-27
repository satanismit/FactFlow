from app.rag.retriever import RetrieverAgent
from app.agents.generator import LLMGeneratorAgent
import os

def main():
    print("Initializing Agents...")
    try:
        retriever = RetrieverAgent()
        generator = LLMGeneratorAgent()
        
        query = "What is the FactFlow system architecture?"
        print(f"\nQuery: {query}")
        
        # Step 2: Retrieve
        print("Retrieving documents...")
        results = retriever.retrieve(query)
        print(f"Retrieved {len(results)} chunks.")
        
        # Step 3: Generate
        print("Generating answer...")
        answer = generator.generate(query, results)
        
        print("\n=== Generated Answer ===")
        print(answer)
        print("========================")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

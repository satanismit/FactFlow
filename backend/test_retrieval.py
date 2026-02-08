from app.rag.retriever import RetrieverAgent
from app.agents.generator import LLMGeneratorAgent
import os

def test_query(retriever, generator, query):
    """Test a single query and display results"""
    print("\n" + "=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    
    # Retrieve
    results = retriever.retrieve(query)
    print(f"\nRetrieved {len(results)} chunks")
    
    # Show what was retrieved
    print("\nTop retrieved content preview:")
    for i, doc in enumerate(results[:2]):  # Show top 2
        content = doc.get('content', '')[:200]  # First 200 chars
        metadata = doc.get('metadata', {})
        print(f"\n   Chunk {i+1} (Page {metadata.get('page', 'N/A')}):")
        print(f"   {content}...")
    
    # Generate answer
    print("\nGenerating answer...")
    answer = generator.generate(query, results)
    
    print("\n" + "=" * 80)
    print("ANSWER:")
    print("=" * 80)
    print(answer)
    print("=" * 80)

def main():
    print("FactFlow System Test")
    print("Testing multiple queries to verify retrieval...\n")
    
    try:
        retriever = RetrieverAgent()
        generator = LLMGeneratorAgent()
        
        # Test different queries
        queries = [
            "What is IPSec?",  # This should work based on retrieved chunks
            "What is encryption?",
            "What is a network protocol?",
            "Explain TCP/IP",
            "What is the OSI model?"
        ]
        
        for query in queries:
            test_query(retriever, generator, query)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

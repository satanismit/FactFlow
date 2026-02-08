from app.rag.retriever import RetrieverAgent
from app.agents.generator import LLMGeneratorAgent
from app.rag.validator import AnswerValidatorAgent
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("Initializing FactFlow System...")
    print("=" * 60)
    
    try:
        retriever = RetrieverAgent()
        generator = LLMGeneratorAgent()
        validator = AnswerValidatorAgent()
        
        # Test Query - Try IPSec first since we know it's in the retrieved chunks
        query ="what is the outline of this course  DESIGN PATTERNS & FRAMEWORKS ?"
        
        print(f"\nQuery: {query}\n")
        
        # Step 1: Retrieve
        print("Retrieving relevant documents...")
        results = retriever.retrieve(query)
        print(f"   Retrieved {len(results)} chunks\n")
        
        # Step 2: Generate Answer
        print("Generating answer...\n")
        answer = generator.generate(query, results)
        
        # Step 3: Validate Answer
        print("Validating answer...\n")
        validation_result = validator.validate(answer, results)
        
        # Display Answer
        print("=" * 60)
        print("ANSWER:")
        print("=" * 60)
        print(answer)
        print("=" * 60)
        
        # Display Trust Score
        print("\n" + "=" * 60)
        print("TRUST SCORE:")
        print("=" * 60)
        trust_score = validation_result['trust_score']
        decision = validation_result['decision']
        components = validation_result['components']
        
        print(f"Trust Score: {trust_score}")
        print(f"Decision: {decision.upper()}")
        print(f"\nComponents:")
        print(f"   - Similarity Score: {components['similarity']}")
        print(f"   - Source Score: {components['source_score']}")
        print(f"   - Freshness Score: {components['freshness_score']}")
        print("=" * 60)
        
        # Optional: Show sources
        print("\nSources:")
        for i, doc in enumerate(results[:3]):  # Show top 3 sources
            metadata = doc.get('metadata', {})
            print(f"   {i+1}. {metadata.get('source', 'Unknown')} - Page {metadata.get('page', 'N/A')}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

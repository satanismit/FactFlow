# Implementation Plan - Step 3: LLM Answer Generator Agent

## Goal Description
Implement the **LLM Answer Generator Agent**, which is responsible for synthesizing an answer solely based on the retrieved documents. This agent must **not** hallucinate information outside of the provided context and must cite its sources. It does *not* validate the answer (that is Agent 4's job).

## User Review Required
> [!IMPORTANT]
> **LLM Provider Selection**: This plan assumes the use of **OpenAI (GPT-4o or GPT-3.5-turbo)** for generation.
> You must provide an `OPENAI_API_KEY` in your `.env` file.
> *Alternative*: If you prefer Google Gemini or Anthropic, please let me know, and I will adjust the dependencies.

## Proposed Changes

### Dependencies
#### [MODIFY] [requirements.txt](file:///d:/Projects/FactFlow/FactFlow/backend/requirements.txt)
- Add `langchain-openai` (or appropriate provider package).

### Configuration
#### [MODIFY] [.env](file:///d:/Projects/FactFlow/FactFlow/backend/.env)
- Add `OPENAI_API_KEY=sk-...`
- Add `LLM_MODEL_NAME=gpt-4o-mini` (or similar).

### Core Logic

#### [NEW] [backend/app/core/prompts.py](file:///d:/Projects/FactFlow/FactFlow/backend/app/core/prompts.py)
- Define the **System Prompt** strictly enforcing:
    1.  Role: "You are an assistant that answers strictly from the provided context."
    2.  Constraint: "Do not use outside knowledge."
    3.  Format: "Include citations [Source: ID]."

#### [NEW] [backend/app/agents/generator.py](file:///d:/Projects/FactFlow/FactFlow/backend/app/agents/generator.py)
- Create `LLMGeneratorAgent` class.
- **Input**: `query` (str), `retrieved_docs` (List[Dict]).
- **Process**:
    1.  Format documents into a string context.
    2.  Construct the prompt with `SystemMessage` and `HumanMessage`.
    3.  Invoke the LLM.
- **Output**: Draft answer string.

#### [MODIFY] [backend/main.py](file:///d:/Projects/FactFlow/FactFlow/backend/main.py)
- Initialize `LLMGeneratorAgent`.
- Connect the output of `RetrieverAgent` (Step 2) into `LLMGeneratorAgent` (Step 3).
- Print the generated answer.

## Verification Plan

### Automated Tests
- Run `python backend/main.py`.
- **Input**: A query like "What is the FactFlow architecture?" (assuming we have some indexed docs about it).
- **Expected Output**: A coherent answer referencing the content of the retrieved chunks.

### Manual Verification
- **Hallucination Check**: Ask a question about something *not* in the documents. The agent should refuse to answer or state it doesn't know.
- **Citation Check**: Ensure `[Source: ...]` tags appear in the output.

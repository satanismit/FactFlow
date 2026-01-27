# FactFlow — Agent Contracts

## Query Preprocessor Agent
**Input:** Raw user query
**Output:** Cleaned & normalized query

---

## Retriever Agent
**Input:** Processed query
**Output:** Top-K document chunks + metadata

---

## LLM Answer Generator Agent
**Input:** Retrieved documents
**Output:** Draft answer

---

## Answer Validator Agent
**Input:** Draft answer + retrieved documents
**Output:** Trust score + trust decision

---

## Hallucination Detector Agent
**Input:** Untrusted answer + documents
**Output:** Hallucination flag / safe decision

---

## Knowledge Refresh Agent
**Input:** Stale knowledge alert
**Output:** Updated vector index

---

## Document Watcher Agent
**Input:** Document store
**Output:** Stale / fresh signal

# AXIOMAI — Complete Project Blueprint

---

## 1. PRODUCT OVERVIEW

### What It Does
AXIOMAI is a **production-grade, agentic Retrieval-Augmented Generation (RAG) system** that answers user queries by retrieving information from ingested documents, generating LLM-powered answers, and then rigorously validating those answers before delivering them. Unlike basic RAG implementations, AXIOMAI treats every answer as "untrusted until proven otherwise." It computes a Trust Score, detects hallucinations at the claim level, and can autonomously refresh stale knowledge — all driven by a multi-agent architecture where each agent has a single, well-defined responsibility. The system is designed for domains where accuracy is non-negotiable: legal research, medical references, compliance, education, and enterprise knowledge bases.

### Target Users
| Attribute | Detail |
|---|---|
| **Primary** | Enterprise knowledge teams, compliance officers, legal/medical researchers (30–55, non-technical to semi-technical) |
| **Secondary** | AI/ML engineers building trustworthy RAG pipelines (25–40, highly technical) |
| **Tertiary** | EdTech platforms needing verified Q&A over course material |
| **Geography** | Global, English-first |

### Core Problem
LLMs hallucinate. Standard RAG pipelines silently pass low-confidence or fabricated answers. In high-stakes domains (legal, medical, compliance), a single wrong answer can cause lawsuits, regulatory fines, or patient harm. **There is no mainstream, open-source RAG system that treats trust as a first-class citizen with automated hallucination detection and self-healing knowledge.**

### Real-World Use Cases
1. **Legal firm** ingests 500+ case law PDFs → lawyers query in natural language → get cited, trust-scored answers
2. **Hospital** ingests clinical guidelines → doctors verify drug interactions → system refuses to answer if evidence is insufficient
3. **University** ingests course materials → students ask questions → system cites exact pages, flags outdated syllabi
4. **Compliance team** ingests regulatory docs → auditors query policy → system auto-refreshes when regulations update

### User Journey
```
Sign Up → Upload Documents → System Indexes (Vector DB)
    → User Asks Question → Retrieval → Generation → Validation
        → IF trusted: Answer + Citations + Trust Score
        → IF untrusted: Hallucination Detection → Flag/Refuse
        → IF stale: Auto-Refresh → Re-answer
    → User reviews answer with confidence level
```

---

## 2. FEATURE BREAKDOWN

### Must-Have (MVP)
| Feature | Status |
|---|---|
| Document ingestion (PDF, TXT) | ✅ Done |
| Vector embedding + Pinecone storage | ✅ Done |
| Query → Retrieve → Generate pipeline | ✅ Done |
| Trust Score computation (similarity + sources + freshness) | ✅ Done |
| Hallucination detection (claim-level verification) | ✅ Done |
| Knowledge Refresh Agent (partial/full re-index) | ✅ Done |
| Document Watcher (hash + timestamp staleness) | ✅ Done |
| Structured output contract (answer, citations, trust, status) | 🔲 Pending |
| Query Preprocessor (cleaning, intent detection) | 🔲 Pending |

### Good-to-Have
- Answer caching (avoid re-generating identical queries)
- Conversation memory (multi-turn Q&A)
- Source highlighting (show exact passages used)
- Batch document ingestion with progress tracking
- Export answers as PDF reports

### Advanced / Future
- Multi-modal RAG (images, tables in PDFs)
- Fine-tuned domain embeddings
- Feedback loop (user thumbs-up/down improves ranking)
- A/B testing of different LLM providers
- Real-time document streaming (RSS, webhooks)
- Multi-tenant isolation

### Admin Features
- Dashboard: ingestion status, query volume, trust score distribution
- Document management: add/remove/re-index
- System health: agent latency, error rates
- User management and API key provisioning

### Edge Cases
- Empty vector DB (no documents indexed) → graceful "no context" response ✅ Handled
- Document with no text (scanned image PDF) → needs OCR preprocessing
- Extremely long documents → chunking strategy matters
- Conflicting sources → trust score should reflect disagreement
- Rate-limited LLM API → queue + retry logic
- Pinecone index dimension mismatch after model change → migration needed

---

## 3. TECHNICAL ARCHITECTURE

### Frontend Stack (Future)
| Choice | Why |
|---|---|
| **Next.js 14+ (App Router)** | SSR for SEO, React ecosystem, API routes built-in |
| **Tailwind CSS** | Rapid prototyping, consistent design |
| **shadcn/ui** | Accessible, composable components |
| **Zustand** | Lightweight state management |

### Backend Stack (Current)
| Choice | Why |
|---|---|
| **Python 3.11** | ML/AI ecosystem, LangChain compatibility |
| **LangChain** | Agent abstraction, prompt management, embeddings |
| **FastAPI** (planned) | Async, auto-docs, type-safe |
| **Google Gemini (gemini-1.5-flash)** | Cost-effective, fast, good quality |
| **Pinecone (Serverless)** | Managed vector DB, scales to zero |
| **HuggingFace BGE-small** | Local embeddings, no API cost |

### Database Design

#### Pinecone Vector Store
```
Index: "axiomai" (dimension: 384, metric: cosine)
├── Vector ID: doc_chunk_{hash}
├── Values: [384-dim embedding]
└── Metadata:
    ├── content: str
    ├── source: str (filename)
    ├── page: int
    ├── content_hash: str (SHA256)
    ├── published_at: str (ISO 8601)
    └── ingested_at: str (ISO 8601)
```

#### Future: PostgreSQL (operational data)
```
users          (id, email, role, api_key, created_at)
documents      (id, filename, status, chunk_count, ingested_at)
queries        (id, user_id, query_text, trust_score, decision, created_at)
refresh_logs   (id, reason, refresh_type, doc_count, timestamp)
```

### Authentication
- **Phase 1**: API key-based (simple, sufficient for internal/demo)
- **Phase 2**: JWT + OAuth 2.0 (Google/GitHub SSO)
- **Phase 3**: Role-based access control (admin, user, viewer)

### API Structure (Planned)
```
POST /api/v1/query          → Ask a question
POST /api/v1/ingest         → Upload documents
GET  /api/v1/documents      → List indexed documents
POST /api/v1/refresh        → Trigger manual refresh
GET  /api/v1/health         → System status
GET  /api/v1/metrics        → Trust score distribution
```

### State Management
- **Backend**: Stateless request handling; agent state lives in function scope
- **Frontend** (future): Zustand for query history, active filters, UI state

### Caching Strategy
- **Embedding cache**: HuggingFace local model cache (`~/.cache/huggingface/`)
- **Query cache** (future): Redis — hash(query) → cached answer (TTL: 1 hour)
- **Document hash cache**: In-memory dict during watcher runs

### File Storage
- **Local**: `backend/data/` for raw source documents
- **Future**: S3/GCS bucket with signed URLs for upload/download

---

## 4. SYSTEM DESIGN

### High-Level Architecture
```
┌──────────────┐
│   User Query │
└──────┬───────┘
       ▼
┌──────────────┐
│  Preprocessor│ ← Clean, normalize, detect intent
└──────┬───────┘
       ▼
┌──────────────┐     ┌──────────────┐
│   Retriever  │────▶│  Pinecone DB │
└──────┬───────┘     └──────────────┘
       ▼
┌──────────────┐     ┌──────────────┐
│  Generator   │────▶│  Gemini LLM  │
└──────┬───────┘     └──────────────┘
       ▼
┌──────────────┐
│  Validator   │ ← Trust Score (0–1)
└──────┬───────┘
       │
       ├─── Trusted ──▶ Return Answer + Citations
       │
       └─── Untrusted ──▶ ┌────────────────────┐
                          │ Hallucination Det.  │
                          └────────┬───────────┘
                                  ▼
                          ┌────────────────────┐
                          │ Knowledge Refresh   │
                          └────────────────────┘
                                  ▲
                          ┌────────────────────┐
                          │ Document Watcher    │ (Background)
                          └────────────────────┘
```

### Data Flow
1. Query enters → cleaned by Preprocessor
2. Preprocessor output → embedded → top-K retrieval from Pinecone
3. Retrieved chunks + query → Gemini generates draft answer
4. Draft answer + chunks → Validator computes Trust Score
5. If trusted → structured response returned
6. If untrusted → Hallucination Detector splits into claims, verifies each
7. Document Watcher periodically checks for hash/timestamp staleness
8. If stale → Knowledge Refresh Agent re-indexes affected documents

### Scalability
| Concern | Solution |
|---|---|
| Embedding bottleneck | Batch embedding, GPU acceleration, or switch to API-based embeddings |
| Pinecone limits | Serverless auto-scales; shard by namespace for multi-tenant |
| LLM rate limits | Queue with exponential backoff; provider fallback (Gemini → OpenAI) |
| Concurrent queries | FastAPI async handlers; horizontal pod scaling |

### Security
- API keys stored in `.env`, never committed (`.gitignore` ✅)
- Input sanitization in Preprocessor (prevent prompt injection)
- Output filtering (no PII leakage from documents)
- HTTPS-only in production
- Pinecone API key rotation policy

### Rate Limiting
- Per-user: 60 queries/minute
- Per-IP: 100 requests/minute
- Global: Circuit breaker on LLM API failures

### Logging & Monitoring
- **Current**: Print-based logging with timestamps ✅
- **Phase 2**: Python `logging` module → structured JSON logs
- **Phase 3**: ELK stack or Datadog; alert on trust score degradation

---

## 5. DEPLOYMENT STRATEGY

### Hosting Options
| Option | Cost | Best For |
|---|---|---|
| **Railway / Render** | $5–25/mo | MVP, demo, small teams |
| **AWS (ECS + Lambda)** | $20–100/mo | Production, scalability |
| **GCP Cloud Run** | Pay-per-use | Cost-optimized, auto-scale |
| **Self-hosted (Docker)** | Hardware cost | Enterprise, data sovereignty |

### CI/CD
```
GitHub Push → GitHub Actions
    ├── Lint (ruff/flake8)
    ├── Test (pytest)
    ├── Build Docker image
    └── Deploy to staging → manual promote to prod
```

### Environments
| Environment | Purpose | Database |
|---|---|---|
| `dev` | Local development | Pinecone dev index |
| `staging` | Pre-release testing | Pinecone staging index |
| `prod` | Live users | Pinecone prod index |

### Versioning
- **API**: URL-based (`/api/v1/`, `/api/v2/`)
- **Code**: Semantic versioning (`v1.2.3`)
- **Git**: Feature branches → PR → `main`

---

## 6. MONETIZATION MODEL

### Pricing Strategy
| Tier | Queries/mo | Documents | Price |
|---|---|---|---|
| **Free** | 50 | 10 | $0 |
| **Pro** | 1,000 | 100 | $29/mo |
| **Team** | 10,000 | 500 | $99/mo |
| **Enterprise** | Unlimited | Unlimited | Custom |

### Free vs Paid Limits
- Free: BGE-small embeddings, basic trust score, 5 chunks/query
- Paid: Choice of embedding model, full hallucination detection, 20 chunks/query, priority refresh

### Growth Strategy
1. Open-source the core agents (community + credibility)
2. Offer hosted version with managed Pinecone + LLM
3. Enterprise: On-premise deployment, custom integrations, SLA
4. Content marketing: "Why RAG without trust scoring is dangerous"

---

## 7. RISKS & FAILURE POINTS

### Technical Risks
| Risk | Severity | Mitigation |
|---|---|---|
| LLM API downtime | High | Provider fallback chain |
| Pinecone outage | High | Local FAISS fallback |
| Embedding model deprecation | Medium | Abstract embedding layer |
| Prompt injection attacks | High | Input sanitization + output filtering |

### Product Risks
- Users may not understand trust scores → need clear UX explanations
- "Refused" answers frustrate users → need graceful degradation
- Document ingestion friction → need drag-and-drop UI

### Scaling Risks
- Embedding large document sets is slow locally → need GPU or API embeddings
- Re-indexing 10K+ documents takes hours → need background job queue
- Multi-tenant data isolation is complex → namespace strategy

### Legal / Privacy Risks
- Documents may contain PII → need data processing agreement
- GDPR: Right to deletion must cascade to vector DB
- Medical/legal domains may require compliance certifications

---

## 8. DEVELOPMENT ROADMAP

### Phase 1 — Core Agents ✅ (Done)
- [x] Retriever Agent
- [x] Generator Agent (Gemini)
- [x] Validator Agent (Trust Score)
- [x] Hallucination Detector Agent
- [x] Knowledge Refresh Agent
- [x] Document Watcher Agent
- [x] PDF ingestion pipeline

### Phase 2 — Production Hardening (Weeks 3–4)
- [ ] Query Preprocessor Agent (cleaning + intent detection)
- [ ] Agent Orchestrator (graph-based workflow with loops)
- [ ] Structured output contract enforcement
- [ ] FastAPI endpoints
- [ ] Error handling + retries
- [ ] Logging upgrade (structured JSON)
- [ ] Unit tests for all agents

### Phase 3 — Frontend & Deployment (Weeks 5–6)
- [ ] Next.js frontend with query UI
- [ ] Document upload interface
- [ ] Trust score visualization
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deploy to staging

### Phase 4 — Launch (Week 7–8)
- [ ] Security audit (prompt injection, PII)
- [ ] Performance benchmarking
- [ ] Documentation (API docs, user guide)
- [ ] Landing page
- [ ] Beta launch with 10 users

### Final Launch Checklist
- [ ] All agents tested independently and end-to-end
- [ ] `.env` secrets rotated for production
- [ ] HTTPS configured
- [ ] Rate limiting active
- [ ] Monitoring dashboards live
- [ ] Backup strategy for document store
- [ ] GDPR/privacy policy published

---

## 9. METRICS TO TRACK

### Technical Metrics
| Metric | Target |
|---|---|
| P95 query latency | < 3 seconds |
| Trust score distribution | Mean > 0.7 |
| Hallucination detection rate | > 90% recall |
| Knowledge refresh frequency | < 1/day (stable) |
| Uptime | 99.5% |

### Business Metrics
| Metric | Target |
|---|---|
| Monthly active users | 100 (month 3) |
| Queries per user per day | > 5 |
| Conversion (free → paid) | > 5% |
| Churn rate | < 10%/mo |

### User Engagement Metrics
| Metric | What It Tells You |
|---|---|
| Queries per session | Are users finding value? |
| % of "refused" answers | Is the system too strict? |
| Document upload frequency | Are users investing in the platform? |
| Trust score click-through | Do users understand/care about trust? |

---

## 10. BRUTALLY HONEST CRITIQUE

### Is This Idea Weak?
**No.** The problem is real and growing. Every enterprise adopting LLMs will hit the hallucination wall. The market timing is excellent (2025–2026 is the "reliability era" of AI).

### Where Will It Likely Fail?
1. **User experience**: If the trust score UX is confusing, users will ignore it
2. **Too many "refused" answers**: Users will switch to ChatGPT which "just answers"
3. **Document ingestion friction**: If uploading and indexing is painful, users won't onboard
4. **Performance**: 3+ second latency for a simple question will frustrate users

### Competitors
| Competitor | Strength | AXIOMAI's Edge |
|---|---|---|
| **Perplexity AI** | Fast, great UX | No trust scoring, no custom docs |
| **Azure AI Search** | Enterprise-grade | Expensive, vendor lock-in |
| **LlamaIndex** | Great framework | Framework, not a product; no trust layer |
| **Verba (Weaviate)** | Open-source RAG | No hallucination detection |
| **Vectara** | Managed RAG API | Closed-source, no self-healing |

### How to Differentiate
1. **Trust Score is the moat** — no competitor has a transparent, configurable trust metric
2. **Self-healing knowledge** — auto-refresh when documents change is unique
3. **Claim-level hallucination detection** — goes beyond simple similarity checks
4. **Open-source core + hosted product** — best of both worlds
5. **Domain-specific templates** — pre-configured for legal, medical, education

---

> *"The best RAG system is one that knows when it doesn't know."*
> — AXIOMAI Design Philosophy

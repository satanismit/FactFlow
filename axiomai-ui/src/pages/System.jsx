import React from 'react';

const System = () => {
    return (
        <div style={{ display: 'grid', gap: '2rem', paddingBottom: '4rem' }}>
            <div style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '1rem' }}>
                <h1 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>SYSTEM_ARCHITECTURE</h1>
                <div className="mono" style={{ color: 'var(--color-intelligence)' }}>&gt; LANGGRAPH_PIPELINE_SCHEMATICS</div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>

                {/* Agent 1 */}
                <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-subtle)', background: 'rgba(139, 92, 246, 0.05)' }}>
                        <h2 className="mono" style={{ fontSize: '0.9rem', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between' }}>
                            <span>[NODE: 01]</span>
                            <span style={{ color: 'var(--color-intelligence)' }}>RETRIEVAL_AGENT</span>
                        </h2>
                    </div>
                    <div style={{ padding: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        Utilizes HuggingFace BGE embeddings to perform high-dimensional semantic search in Pinecone. The agent processes natural language queries to fetch the top-K most relevant and mathematically contiguous document chunks.
                    </div>
                </div>

                {/* Agent 2 */}
                <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-subtle)', background: 'rgba(139, 92, 246, 0.05)' }}>
                        <h2 className="mono" style={{ fontSize: '0.9rem', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between' }}>
                            <span>[NODE: 02]</span>
                            <span style={{ color: 'var(--color-intelligence)' }}>LLM_GENERATOR</span>
                        </h2>
                    </div>
                    <div style={{ padding: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        Driven by deterministic inference pipelines. Ingests context assembled by the Retriever and drafts a grounded response. The instruction layer enforces strict adherence to the provided context space.
                    </div>
                </div>

                {/* Agent 3 */}
                <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-subtle)', background: 'rgba(45, 212, 191, 0.05)' }}>
                        <h2 className="mono" style={{ fontSize: '0.9rem', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between' }}>
                            <span>[NODE: 03]</span>
                            <span style={{ color: 'var(--color-trust)' }}>CLAIM_VALIDATOR</span>
                        </h2>
                    </div>
                    <div style={{ padding: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        Decomposes the proposed answer into individual atomic claims. Each claim is mathematically verified against the retrieved context vector. Unsupported claims trigger a "Hallucinated" flag (SYSTEM_HALT).
                    </div>
                </div>

                {/* Agent 4 */}
                <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-subtle)', background: 'rgba(16, 185, 129, 0.05)' }}>
                        <h2 className="mono" style={{ fontSize: '0.9rem', color: 'var(--text-primary)', display: 'flex', justifyContent: 'space-between' }}>
                            <span>[NODE: 04]</span>
                            <span style={{ color: 'var(--status-trusted)' }}>TRUST_SCORER</span>
                        </h2>
                    </div>
                    <div style={{ padding: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        Computes a deterministic Trust Score based on semantic similarity (40%), source diversity (30%), and documentation freshness (30%). Answers below threshold trigger low-confidence warnings.
                    </div>
                </div>

            </div>
        </div>
    );
};

export default System;

import React from 'react';

const Trust = () => {
    return (
        <div style={{ display: 'grid', gap: '2rem', paddingBottom: '4rem' }}>
            <div style={{ borderBottom: '1px solid var(--border-subtle)', paddingBottom: '1rem' }}>
                <h1 style={{ fontSize: '1.5rem', color: 'var(--text-primary)', marginBottom: '0.5rem' }}>TRUST_PROTOCOLS</h1>
                <div className="mono" style={{ color: 'var(--color-trust)' }}>&gt; VERIFICATION_THRESHOLDS & HEALING_MECHANICS</div>
            </div>

            <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '2rem', border: '1px solid var(--color-trust)' }}>
                <div>
                    <h2 className="mono" style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '0.5rem' }}>GLOBAL_AXIOM_THRESHOLD</h2>
                    <div style={{ color: 'var(--text-primary)', fontSize: '1.1rem' }}>Strict mathematical boundary for output qualification.</div>
                </div>
                <div className="mono" style={{ fontSize: '3rem', color: 'var(--color-trust)', textShadow: '0 0 15px var(--color-trust-dim)' }}>
                    0.65
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                <div className="glass-panel" style={{ padding: '1.5rem', borderLeft: '2px solid var(--status-trusted)' }}>
                    <h3 className="mono" style={{ color: 'var(--status-trusted)', marginBottom: '1rem', fontSize: '0.9rem' }}>STATUS: TRUSTED (≥ 0.65)</h3>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        Answers meeting or exceeding the Trust Threshold have been successfully validated across multiple vectors: diverse citation sources, high semantic overlap with user intent, and mathematical validation of all parsed claims.
                    </p>
                </div>
                <div className="glass-panel" style={{ padding: '1.5rem', borderLeft: '2px solid var(--status-risk)' }}>
                    <h3 className="mono" style={{ color: 'var(--status-risk)', marginBottom: '1rem', fontSize: '0.9rem' }}>STATUS: LOW_CONFIDENCE (&lt; 0.65)</h3>
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem' }}>
                        System generated a correct response but lacks diverse sources or uses stale data. Triggers a low confidence warning. Output is presented but flagged for manual review.
                    </p>
                </div>
            </div>

            <div className="glass-panel" style={{ marginTop: '1rem' }}>
                <div style={{ padding: '1rem', borderBottom: '1px solid var(--border-subtle)' }}>
                    <h3 className="mono" style={{ color: 'var(--text-primary)', fontSize: '0.9rem' }}>SELF_HEALING_MECHANICS</h3>
                </div>
                <div style={{ padding: '1.5rem' }}>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem', fontSize: '0.95rem' }}>
                        If an answer fails hallucination detection, AXIOMAI halts output. The Knowledge Refresh Agent engages automatically, re-indexing the problematic document subset and retrying the query generation loop up to 2 times to correct the knowledge gap.
                    </p>
                    <div className="mono" style={{
                        padding: '1rem',
                        background: 'var(--bg-primary)',
                        border: '1px solid var(--border-subtle)',
                        borderRadius: '4px',
                        fontSize: '0.85rem',
                        color: 'var(--text-muted)'
                    }}>
                        <span style={{ color: 'var(--status-risk)' }}>hallucination</span> ➔ <span style={{ color: 'var(--color-trust)' }}>refresh_node</span> ➔ <span style={{ color: 'var(--text-primary)' }}>retrieve_node</span> ➔ <span style={{ color: 'var(--text-primary)' }}>generate_node</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Trust;

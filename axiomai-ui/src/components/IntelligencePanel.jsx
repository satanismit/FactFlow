import React, { useState, useEffect, useRef } from 'react';
import './components.css';

export default function IntelligencePanel({ logs }) {
    const [expanded, setExpanded] = useState(true);
    const scrollRef = useRef(null);

    // Auto-scroll to bottom when logs update
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs, expanded]);

    const togglePanel = () => setExpanded(!expanded);

    const formatLog = (msg) => {
        if (msg.includes('[SYSTEM]')) return <span style={{ color: 'var(--accent-verify)' }}>{msg}</span>;
        if (msg.includes('[WAIT]')) return <span style={{ color: 'var(--status-warning)' }}>{msg}</span>;
        if (msg.includes('[ERROR]')) return <span style={{ color: 'var(--status-risk)' }}>{msg}</span>;
        if (msg.match(/\[RETRIEVER\]|\[GENERATOR\]|\[VALIDATOR\]|\[VERIFIER\]/)) return <span style={{ color: 'var(--accent-trust)' }}>{msg}</span>;
        return msg;
    };

    return (
        <div className={`intelligence-card glass-panel ${expanded ? 'expanded' : 'collapsed'}`}>
            <div className="intelligence-header" onClick={togglePanel} style={{ cursor: 'pointer' }}>
                <h3>Intelligence Reasoning</h3>
                <button className="toggle-btn">
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" strokeWidth="2" fill="none"
                        style={{ transform: expanded ? 'rotate(180deg)' : 'rotate(0deg)', transition: 'transform 0.3s' }}>
                        <polyline points="6 9 12 15 18 9"></polyline>
                    </svg>
                </button>
            </div>

            {expanded && (
                <div className="intelligence-content mono" ref={scrollRef}>
                    {logs && logs.map((log, idx) => (
                        <div key={idx} className="log-entry">
                            {formatLog(log)}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

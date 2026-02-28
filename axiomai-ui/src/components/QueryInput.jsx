import React, { useState } from 'react';
import './components.css';

export default function QueryInput({ onSubmit, disabled }) {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim() && !disabled) {
            onSubmit(query.trim());
            // Don't clear query immediately so user can see what they asked
        }
    };

    return (
        <div className="query-section glass-panel">
            <form className="query-input-wrapper" onSubmit={handleSubmit}>
                <input
                    type="text"
                    className="query-input"
                    placeholder="Ask a question. AXIOMAI will verify before answering."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={disabled}
                />
                <button type="submit" className="submit-query-btn" disabled={disabled || !query.trim()}>
                    <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </form>
        </div>
    );
}

import React from 'react';
import './components.css';

export default function CitationsPanel({ citations }) {
    return (
        <div className="evidence-panel glass-panel">
            <div className="panel-header">
                <h2>Evidence & Citations</h2>
                <div className="count mono">{citations ? citations.length : 0} SOURCES</div>
            </div>

            <div className="scroll-container">
                {(!citations || citations.length === 0) ? (
                    <div className="empty-state">Waiting for query context...</div>
                ) : (
                    <div className="citations-list">
                        {citations.map((cite, idx) => (
                            <div key={idx} className="evidence-card glass-panel">
                                <div className="card-top">
                                    <span className="mono source-name">{cite.source}</span>
                                    <span className="mono match-score">{(cite.similarity * 100).toFixed(0)}% Match</span>
                                </div>
                                {cite.freshness_days !== undefined && (
                                    <div className="freshness mono">{cite.freshness_days} days old</div>
                                )}
                                {cite.snippet && (
                                    <div className="snippet-text">"{cite.snippet}"</div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

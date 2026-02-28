import React from 'react';
import './components.css';

export default function AnswerPanel({ answer, claims }) {
    return (
        <div className="answer-container glass-panel">
            <div className="answer-header">
                <h3>Grounded Response</h3>
                <div className="confidence-tag">OVERALL_VERIFIED</div>
            </div>
            <div className="answer-text">
                <p>{answer}</p>
            </div>

            {claims && claims.length > 0 && (
                <div className="claims-section">
                    <h4 className="mono" style={{ color: 'var(--text-secondary)', marginBottom: '1rem', marginTop: '2rem' }}>CLAIM LEVEL VERIFICATION</h4>
                    <div className="claims-grid">
                        {claims.map((claim, idx) => (
                            <ClaimCard key={idx} claim={claim} />
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

function ClaimCard({ claim }) {
    // mapping status strings from API: 'supported', 'low_confidence', 'hallucinated'
    let statusClass = '';
    let statusIcon = '';
    let statusText = '';

    switch (claim.status) {
        case 'supported':
            statusClass = 'supported';
            statusIcon = '✓';
            statusText = 'VERIFIED';
            break;
        case 'low_confidence':
            statusClass = 'warning';
            statusIcon = '⚠';
            statusText = 'ATTESTATION_LOW';
            break;
        case 'hallucinated':
            statusClass = 'error';
            statusIcon = '✗';
            statusText = 'UNSUPPORTED';
            break;
        default:
            statusClass = 'warning';
            statusIcon = '?';
            statusText = 'UNKNOWN';
    }

    return (
        <div className={`claim-card ${statusClass}`}>
            <div className="claim-header">
                <div className="claim-status">
                    <span className="mono status-icon">{statusIcon}</span>
                    <span className="mono">{statusText}</span>
                </div>
                {claim.evidence_count !== undefined && (
                    <div className="evidence-badge mono">{claim.evidence_count} CITATIONS</div>
                )}
            </div>
            <div className="claim-text">{claim.text}</div>
        </div>
    );
}

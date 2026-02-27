import React, { useEffect, useState } from 'react';
import './components.css';

export default function TrustMeter({ score }) {
    const [offset, setOffset] = useState(283); // 2 * pi * 45 = 282.7
    const radius = 45;
    const circumference = 2 * Math.PI * radius;

    useEffect(() => {
        // Animate the fill
        const newOffset = circumference - (score * circumference);
        setOffset(newOffset);
    }, [score, circumference]);

    let colorClass = 'risk';
    if (score >= 0.65) colorClass = 'trusted';
    else if (score >= 0.45) colorClass = 'warning';

    return (
        <div className="trust-meter-card glass-panel">
            <h3>Trust Score</h3>
            <div className="radial-score-container">
                <svg className="radial-score-svg" viewBox="0 0 100 100">
                    <circle className="score-bg" cx="50" cy="50" r={radius}></circle>
                    <circle
                        className={`score-fill ${colorClass}`}
                        cx="50" cy="50" r={radius}
                        style={{ strokeDasharray: circumference, strokeDashoffset: offset }}
                    ></circle>
                </svg>
                <div className="score-value">
                    <span id="score-number">{score.toFixed(2)}</span>
                    <span className="score-max mono">/1.00</span>
                </div>
            </div>

            <div className="score-breakdown">
                <div className="breakdown-item">
                    <span>Similarity</span>
                    <div className="bar-bg">
                        <div className="bar-fill" style={{ width: `${score > 0 ? (score * 95) : 0}%`, background: 'var(--accent-trust)' }}></div>
                    </div>
                </div>
                <div className="breakdown-item">
                    <span>Diversity</span>
                    <div className="bar-bg">
                        <div className="bar-fill" style={{ width: `${score > 0 ? (score * 80) : 0}%`, background: 'var(--accent-verify)' }}></div>
                    </div>
                </div>
                <div className="breakdown-item">
                    <span>Freshness</span>
                    <div className="bar-bg">
                        <div className="bar-fill" style={{ width: `${score > 0 ? (score * 70) : 0}%`, background: 'var(--accent-trust)' }}></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

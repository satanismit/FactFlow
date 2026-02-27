import React from 'react';
import './components.css';

const STAGES = [
    { id: 'retrieving', label: 'Retrieve' },
    { id: 'generating', label: 'Generate' },
    { id: 'validating', label: 'Validate' },
    { id: 'verifying', label: 'Verify' },
    { id: 'refreshing', label: 'Refresh' }
];

export default function PipelineVisualizer({ phase }) {
    // Determine if a step is active or completed based on current phase
    // 'idle' -> nothing active
    // 'done' -> all completed

    const getStepStatus = (stepId, index) => {
        if (phase === 'idle') return '';
        if (phase === 'done') return 'completed';

        // Find index of current phase
        const currentIndex = STAGES.findIndex(s => s.id === phase);

        if (currentIndex === -1) return ''; // fallback

        if (index < currentIndex) return 'completed';
        if (index === currentIndex) return 'active';
        return '';
    };

    return (
        <div className="pipeline-viz">
            <div className="pipeline-track">
                <div
                    className="pipeline-progress"
                    style={{
                        width: phase === 'done' ? '100%' :
                            phase === 'idle' ? '0%' :
                                `${(STAGES.findIndex(s => s.id === phase) / (STAGES.length - 1)) * 100}%`
                    }}
                ></div>
            </div>
            <div className="pipeline-steps">
                {STAGES.map((step, index) => {
                    const statusClass = getStepStatus(step.id, index);
                    return (
                        <div key={step.id} className={`step ${statusClass}`}>
                            <div className="step-dot">
                                {statusClass === 'active' && <div className="pulse-ring"></div>}
                                {statusClass === 'completed' && (
                                    <svg viewBox="0 0 24 24" width="14" height="14" stroke="white" strokeWidth="3" fill="none">
                                        <polyline points="20 6 9 17 4 12"></polyline>
                                    </svg>
                                )}
                            </div>
                            <span className="mono">{step.label}</span>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

import React from 'react';
import { useQuerySession } from '../context/QuerySessionContext';
import '../index.css';

// Components
import QueryInput from '../components/QueryInput';
import PipelineVisualizer from '../components/PipelineVisualizer';
import AnswerPanel from '../components/AnswerPanel';
import CitationsPanel from '../components/CitationsPanel';
import TrustMeter from '../components/TrustMeter';
import IntelligencePanel from '../components/IntelligencePanel';

const QueryPage = () => {
    const { state, handleQuerySubmit } = useQuerySession();

    return (
        <div style={{ display: 'grid', gridTemplateColumns: 'minmax(250px, 300px) 1fr minmax(280px, 350px)', gap: '2rem', height: '100%' }}>
            {/* Left Panel: Citations & Evidence */}
            <aside style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', overflowY: 'auto' }}>
                <CitationsPanel citations={state.citations} />
            </aside>

            {/* Center Panel: Query, Pipeline, Answer */}
            <main style={{ display: 'flex', flexDirection: 'column', gap: '2rem', flex: 1, minWidth: 0 }}>
                <QueryInput onSubmit={handleQuerySubmit} disabled={state.phase !== 'idle' && state.phase !== 'done'} />

                <PipelineVisualizer phase={state.phase} />

                {state.error && <div style={{ color: 'var(--status-risk)', padding: '1rem' }} className="glass-panel mono">{state.error}</div>}

                {(state.phase === 'done' || state.answer) && !state.error && (
                    <AnswerPanel answer={state.answer} claims={state.claims} />
                )}
            </main>

            {/* Right Panel: Trust & Intelligence */}
            <aside style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', overflowY: 'auto' }}>
                <TrustMeter score={state.trustScore} />
                <IntelligencePanel logs={state.reasoningLog} />
            </aside>
        </div>
    );
};

export default QueryPage;

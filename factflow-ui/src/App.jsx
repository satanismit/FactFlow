import { useState } from 'react';
import './index.css';

// Components (to be implemented)
import QueryInput from './components/QueryInput';
import PipelineVisualizer from './components/PipelineVisualizer';
import AnswerPanel from './components/AnswerPanel';
import CitationsPanel from './components/CitationsPanel';
import TrustMeter from './components/TrustMeter';
import IntelligencePanel from './components/IntelligencePanel';

function App() {
    // Global State Model per requirements
    const [state, setState] = useState({
        phase: "idle", // idle | retrieving | generating | validating | verifying | refreshing | done
        trustScore: 0,
        claims: [],
        citations: [],
        answer: "",
        reasoningLog: ["[SYSTEM] FactFlow initialized.", "[WAIT] Awaiting user query..."],
        error: null
    });

    const handleQuerySubmit = async (query) => {
        if (!query) return;

        // Reset state for new query
        setState({
            phase: "retrieving",
            trustScore: 0,
            claims: [],
            citations: [],
            answer: "",
            reasoningLog: [`[SYSTEM] New query received: "${query}"`],
            error: null
        });

        try {
            // Connect to FastAPI backend
            // Adjust URL based on actual backend port (usually 8000)
            const API_URL = 'http://localhost:8000/api/v1/query';

            // Simulate pipeline progression before actual fetch for UI UX
            // (In a real scenario, Server-Sent Events or WebSockets are better for phase updates,
            // but here we will simulate the feeling of the pipeline while waiting for the single API response)

            const phases = ['generating', 'validating', 'verifying'];
            let currentPhaseIdx = 0;

            const simulateInterval = setInterval(() => {
                if (currentPhaseIdx < phases.length) {
                    setState(prev => ({
                        ...prev,
                        phase: phases[currentPhaseIdx],
                        reasoningLog: [...prev.reasoningLog, `[SYSTEM] Transitioning to ${phases[currentPhaseIdx]}...`]
                    }));
                    currentPhaseIdx++;
                }
            }, 1000);

            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            clearInterval(simulateInterval);

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            // Final state injection
            setState(prev => ({
                ...prev,
                phase: "done",
                trustScore: data.trust_score || 0,
                answer: data.answer || "No logical answer generated.",
                claims: data.claims || [],
                citations: data.citations || [],
                reasoningLog: [...prev.reasoningLog, ...(data.reasoning_log || []), "[SYSTEM] Query resolution complete."]
            }));

        } catch (err) {
            console.error(err);
            setState(prev => ({
                ...prev,
                phase: "idle",
                error: "Failed to connect to FactFlow Intelligence Backend.",
                reasoningLog: [...prev.reasoningLog, `[ERROR] ${err.message}`]
            }));
        }
    };

    return (
        <div className="app-container">
            <header className="app-header glass-panel">
                <div className="logo-group">
                    <span className="logo-text">FactFlow</span>
                    <span className="version-tag mono">v1.2.0</span>
                </div>
                <div className="mono" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ width: 8, height: 8, background: 'var(--status-trusted)', borderRadius: '50%', display: 'inline-block' }}></span>
                    SYSTEM_ONLINE
                </div>
            </header>

            {/* Left Panel: Citations & Evidence */}
            <aside className="left-panel">
                <CitationsPanel citations={state.citations} />
            </aside>

            {/* Center Panel: Query, Pipeline, Answer */}
            <main className="center-panel">
                <QueryInput onSubmit={handleQuerySubmit} disabled={state.phase !== 'idle' && state.phase !== 'done'} />
                <PipelineVisualizer phase={state.phase} />

                {state.error && <div style={{ color: 'var(--status-risk)', padding: '1rem' }} className="glass-panel mono">{state.error}</div>}

                {(state.phase === 'done' || state.answer) && !state.error && (
                    <AnswerPanel answer={state.answer} claims={state.claims} />
                )}
            </main>

            {/* Right Panel: Trust & Intelligence */}
            <aside className="right-panel">
                <TrustMeter score={state.trustScore} />
                <IntelligencePanel logs={state.reasoningLog} />
            </aside>
        </div>
    );
}

export default App;

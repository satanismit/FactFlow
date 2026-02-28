import React, { createContext, useState, useContext } from 'react';

const QuerySessionContext = createContext(null);

export const QuerySessionProvider = ({ children }) => {
    const [state, setState] = useState({
        phase: "idle", // idle | retrieving | generating | validating | verifying | refreshing | done
        trustScore: 0,
        claims: [],
        citations: [],
        answer: "",
        reasoningLog: ["[SYSTEM] AXIOMAI initialized.", "[WAIT] Awaiting user query..."],
        error: null
    });

    const handleQuerySubmit = async (query) => {
        if (!query) return;

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
            const API_URL = 'http://localhost:8000/api/v1/query';

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
                error: "Failed to connect to AXIOMAI Intelligence Backend.",
                reasoningLog: [...prev.reasoningLog, `[ERROR] ${err.message}`]
            }));
        }
    };

    return (
        <QuerySessionContext.Provider value={{ state, handleQuerySubmit }}>
            {children}
        </QuerySessionContext.Provider>
    );
};

export const useQuerySession = () => useContext(QuerySessionContext);

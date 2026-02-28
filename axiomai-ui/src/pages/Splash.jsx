import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../index.css';

const Splash = () => {
    const navigate = useNavigate();
    const [opacity, setOpacity] = useState(1);

    useEffect(() => {
        // Only show once per session
        if (sessionStorage.getItem('axiomai_booted')) {
            navigate('/home', { replace: true });
            return;
        }

        // Boot sequence length
        const timer = setTimeout(() => {
            setOpacity(0); // Fade out transition
            setTimeout(() => {
                sessionStorage.setItem('axiomai_booted', 'true');
                // Explicitly redirect to /home to preserve brand-first informational experience
                navigate('/home', { replace: true });
            }, 600); // Wait for fade out
        }, 1800); // 1.8 seconds of logo

        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <div
            style={{
                position: 'fixed',
                inset: 0,
                backgroundColor: 'var(--bg-primary)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 9999,
                opacity: opacity,
                transition: 'opacity 0.6s ease-in-out'
            }}
        >
            <div style={{ textAlign: 'center' }}>
                <img
                    src="/logo.png"
                    alt="AXIOMAI Core"
                    style={{
                        height: '100px',
                        mixBlendMode: 'lighten',
                        filter: 'drop-shadow(0 0 25px var(--color-trust-dim))',
                        animation: 'fadeIn 1s ease-out'
                    }}
                />
            </div>
        </div>
    );
};

export default Splash;

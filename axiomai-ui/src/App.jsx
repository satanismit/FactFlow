import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Layout & Context
import Layout from './components/Layout';

// Pages
import Splash from './pages/Splash';
import Home from './pages/Home';
import QueryPage from './pages/QueryPage';
import System from './pages/System';
import Trust from './pages/Trust';

function App() {
    return (
        <Routes>
            <Route path="/" element={<Splash />} />
            <Route element={<Layout />}>
                <Route path="/home" element={<Home />} />
                <Route path="/query" element={<QueryPage />} />
                <Route path="/system" element={<System />} />
                <Route path="/trust" element={<Trust />} />
            </Route>
            <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
    );
}

export default App;

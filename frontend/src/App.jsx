import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Predict from './pages/Predict';
import History from './pages/History';

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/predict"   element={<Predict />} />
            <Route path="/history"   element={<History />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

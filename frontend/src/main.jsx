import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './styles.css';
import AppShell from './ui/AppShell.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Inbox from './pages/Inbox.jsx';
import ThreadView from './pages/ThreadView.jsx';
import CustomerView from './pages/CustomerView.jsx';
import AIAnalysis from './pages/AIAnalysis.jsx';
import KnowledgeSearch from './pages/KnowledgeSearch.jsx';
import Analytics from './pages/Analytics.jsx';
import Settings from './pages/Settings.jsx';

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<AppShell />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/inbox" element={<Inbox />} />
          <Route path="/threads/:threadId" element={<ThreadView />} />
          <Route path="/customers/:contactId" element={<CustomerView />} />
          <Route path="/ai" element={<AIAnalysis />} />
          <Route path="/knowledge" element={<KnowledgeSearch />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);

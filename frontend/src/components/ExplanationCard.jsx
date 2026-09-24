import React, { useState } from 'react';
import { FileText, User, BarChart2, Copy, Check } from 'lucide-react';

export default function ExplanationCard({ explanations = {}, llmData = {} }) {
  const [activeTab, setActiveTab] = useState('officer');
  const [copied, setCopied] = useState(false);

  const tabs = [
    { key: 'officer',   label: 'Officer Note',    icon: FileText  },
    { key: 'customer',  label: 'Customer Letter',  icon: User      },
    { key: 'summary',   label: 'Risk Summary',     icon: BarChart2 },
  ];

  const getText = () => {
    if (activeTab === 'officer')  return explanations?.officer_note?.explanation  || llmData?.loan_officer_notes  || llmData?.summary || '';
    if (activeTab === 'customer') return explanations?.customer_letter?.explanation || llmData?.customer_explanation || '';
    if (activeTab === 'summary')  return explanations?.risk_summary?.explanation   || llmData?.summary             || '';
    return '';
  };

  const text = getText();

  const handleCopy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="card" style={{ marginTop: 24 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
        <span className="card-title" style={{ marginBottom: 0 }}>GPT-4 Explanation</span>
        {text && (
          <button className="btn btn-ghost" style={{ padding: '6px 12px', fontSize: 12 }} onClick={handleCopy}>
            {copied ? <Check size={13} /> : <Copy size={13} />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        )}
      </div>

      <div className="tabs">
        {tabs.map(({ key, label, icon: Icon }) => (
          <button key={key} className={`tab ${activeTab === key ? 'active' : ''}`}
            onClick={() => setActiveTab(key)}
            style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
            <Icon size={13} />{label}
          </button>
        ))}
      </div>

      {text ? (
        <div style={{
          background: 'var(--bg-secondary)', border: '1px solid var(--border)',
          borderRadius: 8, padding: '16px 20px', fontSize: 13,
          color: 'var(--text-secondary)', lineHeight: 1.8, whiteSpace: 'pre-wrap', minHeight: 120,
        }}>
          {text}
        </div>
      ) : (
        <div style={{
          background: 'var(--bg-secondary)', border: '1px solid var(--border)',
          borderRadius: 8, padding: '40px 20px', textAlign: 'center',
          color: 'var(--text-muted)', fontSize: 13,
        }}>
          No explanation available — OpenAI connection failed.
        </div>
      )}
    </div>
  );
}
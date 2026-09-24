import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import { Filter, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const PAGE_SIZE = 20;

function DecisionBadge({ decision }) {
  const map = { APPROVE: 'badge-approve', DECLINE: 'badge-decline', REVIEW: 'badge-review' };
  return <span className={`badge ${map[decision] || 'badge-review'}`}>{decision}</span>;
}

function RiskBadge({ level }) {
  const map = { 'Low': 'badge-low', 'Medium': 'badge-medium', 'High': 'badge-high', 'Very High': 'badge-very-high' };
  return <span className={`badge ${map[level] || 'badge-medium'}`}>{level}</span>;
}

export default function History() {
  const [records,  setRecords]  = useState([]);
  const [total,    setTotal]    = useState(0);
  const [page,     setPage]     = useState(0);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');
  const [filters,  setFilters]  = useState({ decision: '', risk_level: '' });

  const fetchHistory = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const params = new URLSearchParams({
        limit:  PAGE_SIZE,
        offset: page * PAGE_SIZE,
      });
      if (filters.decision)   params.append('decision',   filters.decision);
      if (filters.risk_level) params.append('risk_level', filters.risk_level);

      const { data } = await axios.get(`${API}/history?${params}`);
      setRecords(data.records || []);
      setTotal(data.total || 0);
    } catch {
      setError('Failed to load history. Ensure the API is running.');
    } finally {
      setLoading(false);
    }
  }, [page, filters]);

  useEffect(() => { fetchHistory(); }, [fetchHistory]);

  const totalPages = Math.ceil(total / PAGE_SIZE);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(0);
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Prediction History</h1>
        <p className="page-subtitle">{total} total predictions logged in PostgreSQL</p>
      </div>

      {/* Filter bar */}
      <div className="card" style={{ marginBottom: 20, padding: '16px 20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: 'var(--text-muted)', fontSize: 13 }}>
            <Filter size={14} /> Filters
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <label style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Decision:</label>
            <select
              className="form-select"
              style={{ width: 140, padding: '6px 10px' }}
              value={filters.decision}
              onChange={e => handleFilterChange('decision', e.target.value)}
            >
              <option value="">All</option>
              <option value="APPROVE">Approve</option>
              <option value="REVIEW">Review</option>
              <option value="DECLINE">Decline</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <label style={{ fontSize: 12, color: 'var(--text-secondary)' }}>Risk Level:</label>
            <select
              className="form-select"
              style={{ width: 140, padding: '6px 10px' }}
              value={filters.risk_level}
              onChange={e => handleFilterChange('risk_level', e.target.value)}
            >
              <option value="">All</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Very High">Very High</option>
            </select>
          </div>

          <button className="btn btn-ghost" style={{ padding: '6px 12px', marginLeft: 'auto' }} onClick={fetchHistory}>
            <RefreshCw size={13} /> Refresh
          </button>
        </div>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {/* Table */}
      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 60, gap: 12 }}>
          <div className="spinner" />
          <span style={{ color: 'var(--text-secondary)' }}>Loading...</span>
        </div>
      ) : records.length === 0 ? (
        <div className="card">
          <div className="empty-state">
            <p>No predictions found. Try adjusting filters or submit a prediction first.</p>
          </div>
        </div>
      ) : (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Loan Amount</th>
                  <th>Annual Income</th>
                  <th>DTI</th>
                  <th>Default Probability</th>
                  <th>Risk Level</th>
                  <th>Decision</th>
                  <th>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {records.map(r => (
                  <tr key={r.id}>
                    <td className="mono" style={{ color: 'var(--text-muted)' }}>#{r.id}</td>
                    <td className="mono">${r.loan_amount?.toLocaleString() ?? '—'}</td>
                    <td className="mono">${r.annual_income?.toLocaleString() ?? '—'}</td>
                    <td className="mono">{r.dti?.toFixed(1) ?? '—'}%</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <div style={{
                          width: 48, height: 4, borderRadius: 2,
                          background: 'var(--border)', overflow: 'hidden',
                        }}>
                          <div style={{
                            height: '100%',
                            width: `${(r.default_probability * 100).toFixed(0)}%`,
                            background: r.default_probability > 0.7 ? '#ef4444' : r.default_probability > 0.45 ? '#f59e0b' : '#10b981',
                            borderRadius: 2,
                          }} />
                        </div>
                        <span className="mono">{(r.default_probability * 100).toFixed(1)}%</span>
                      </div>
                    </td>
                    <td><RiskBadge level={r.risk_level} /></td>
                    <td><DecisionBadge decision={r.decision} /></td>
                    <td style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      {r.created_at ? new Date(r.created_at).toLocaleString() : '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 16 }}>
              <span style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                Page {page + 1} of {totalPages} · {total} total records
              </span>
              <div style={{ display: 'flex', gap: 8 }}>
                <button className="btn btn-ghost" style={{ padding: '6px 12px' }}
                  onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0}>
                  <ChevronLeft size={14} /> Prev
                </button>
                <button className="btn btn-ghost" style={{ padding: '6px 12px' }}
                  onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1}>
                  Next <ChevronRight size={14} />
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BrainCircuit, History, ShieldCheck } from 'lucide-react';

const links = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/predict',   icon: BrainCircuit,    label: 'Predict'   },
  { to: '/history',   icon: History,         label: 'History'   },
];

export default function Navbar() {
  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, bottom: 0, width: 240,
      background: '#0d1526', borderRight: '1px solid var(--border)',
      display: 'flex', flexDirection: 'column', padding: '24px 0', zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{ padding: '0 20px 28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <ShieldCheck size={18} color="#fff" />
          </div>
          <div>
            <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.2 }}>
              Risk Explainer
            </div>
            <div style={{ fontSize: 10, color: 'var(--text-muted)', letterSpacing: '0.5px' }}>
              LLM · ENSEMBLE v2
            </div>
          </div>
        </div>
      </div>

      {/* Section label */}
      <div style={{ padding: '0 20px 8px', fontSize: 10, fontWeight: 600, color: 'var(--text-muted)', letterSpacing: '1px', textTransform: 'uppercase' }}>
        Menu
      </div>

      {/* Nav links */}
      <div style={{ flex: 1, padding: '0 12px' }}>
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} style={{ textDecoration: 'none' }}>
            {({ isActive }) => (
              <div style={{
                display: 'flex', alignItems: 'center', gap: 10,
                padding: '10px 12px', borderRadius: 8, marginBottom: 4,
                background: isActive ? 'var(--accent-glow)' : 'transparent',
                color: isActive ? 'var(--accent)' : 'var(--text-secondary)',
                fontWeight: isActive ? 600 : 400, fontSize: 14,
                transition: 'all 0.15s', cursor: 'pointer',
                borderLeft: isActive ? '2px solid var(--accent)' : '2px solid transparent',
              }}>
                <Icon size={16} />
                {label}
              </div>
            )}
          </NavLink>
        ))}
      </div>

      {/* Footer */}
      <div style={{ padding: '16px 20px', borderTop: '1px solid var(--border)' }}>
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>XGBoost · LightGBM · CatBoost</div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Meta: Logistic Regression</div>
      </div>
    </nav>
  );
}

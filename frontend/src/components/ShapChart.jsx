import React from 'react';

export default function ShapChart({ shapValues = {} }) {
  const riskFactors      = shapValues.risk_factors      || [];
  const protectiveFactors = shapValues.protective_factors || [];

  // Combine and sort by absolute shap value
  const all = [
    ...riskFactors.map(f => ({ ...f, direction: 'risk' })),
    ...protectiveFactors.map(f => ({ ...f, direction: 'protective' })),
  ]
    .sort((a, b) => Math.abs(b.shap_value) - Math.abs(a.shap_value))
    .slice(0, 10);

  if (all.length === 0) {
    return (
      <div className="empty-state">
        <p>No SHAP values available</p>
      </div>
    );
  }

  const maxAbs = Math.max(...all.map(f => Math.abs(f.shap_value)));

  const formatFeature = (name) =>
    name.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      {/* Legend */}
      <div style={{ display: 'flex', gap: 16, marginBottom: 4 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--text-muted)' }}>
          <div style={{ width: 10, height: 10, borderRadius: 2, background: '#ef4444' }} />
          Increases Risk
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 11, color: 'var(--text-muted)' }}>
          <div style={{ width: 10, height: 10, borderRadius: 2, background: '#10b981' }} />
          Reduces Risk
        </div>
      </div>

      {all.map((f, i) => {
        const isRisk = f.direction === 'risk';
        const barColor = isRisk ? '#ef4444' : '#10b981';
        const barWidth = (Math.abs(f.shap_value) / maxAbs) * 100;

        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {/* Feature name */}
            <div style={{
              width: 160, fontSize: 12, color: 'var(--text-secondary)',
              textAlign: 'right', flexShrink: 0, whiteSpace: 'nowrap',
              overflow: 'hidden', textOverflow: 'ellipsis',
            }} title={formatFeature(f.feature)}>
              {formatFeature(f.feature)}
            </div>

            {/* Bar */}
            <div style={{ flex: 1, height: 22, background: 'var(--bg-secondary)', borderRadius: 4, overflow: 'hidden', position: 'relative' }}>
              <div style={{
                position: 'absolute', top: 0, bottom: 0,
                left: isRisk ? 0 : undefined,
                right: isRisk ? undefined : 0,
                width: `${barWidth}%`,
                background: `${barColor}`,
                borderRadius: 4,
                opacity: 0.85,
                transition: 'width 0.4s ease',
              }} />
              <div style={{
                position: 'absolute', top: 0, bottom: 0, left: 0, right: 0,
                display: 'flex', alignItems: 'center',
                padding: '0 8px', justifyContent: isRisk ? 'flex-start' : 'flex-end',
              }}>
                <span style={{ fontSize: 10, fontFamily: 'var(--font-mono)', color: '#fff', fontWeight: 600 }}>
                  {isRisk ? '+' : ''}{f.shap_value.toFixed(3)}
                </span>
              </div>
            </div>

            {/* Value */}
            <div style={{ width: 70, fontSize: 11, color: 'var(--text-muted)', flexShrink: 0, fontFamily: 'var(--font-mono)' }}>
              {String(f.value).slice(0, 8)}
            </div>
          </div>
        );
      })}
    </div>
  );
}

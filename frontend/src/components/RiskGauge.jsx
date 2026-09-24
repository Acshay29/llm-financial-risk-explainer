import React from 'react';

export default function RiskGauge({ probability = 0 }) {
  const pct = Math.round(probability * 100);
  const angle = -135 + (pct / 100) * 270;
  const cx = 100, cy = 100, r = 72;

  const getColor = () => {
    if (pct < 20) return '#10b981';
    if (pct < 45) return '#f59e0b';
    if (pct < 70) return '#f97316';
    return '#ef4444';
  };

  const getLabel = () => {
    if (pct < 20) return 'LOW RISK';
    if (pct < 45) return 'MEDIUM RISK';
    if (pct < 70) return 'HIGH RISK';
    return 'VERY HIGH';
  };

  const polarToCartesian = (angleDeg) => {
    const rad = (angleDeg - 90) * Math.PI / 180;
    return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
  };

  const arcPath = (startAngle, endAngle) => {
    const s = polarToCartesian(startAngle);
    const e = polarToCartesian(endAngle);
    const large = endAngle - startAngle > 180 ? 1 : 0;
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
  };

  const color = getColor();
  const fillEnd = -135 + (pct / 100) * 270;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <svg width="200" height="155" viewBox="0 0 200 155">
        {/* Glow filter */}
        <defs>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge><feMergeNode in="coloredBlur" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>

        {/* Track */}
        <path d={arcPath(-135, 135)} fill="none" stroke="var(--border)" strokeWidth="10" strokeLinecap="round" />

        {/* Fill */}
        {pct > 0 && (
          <path d={arcPath(-135, fillEnd)} fill="none" stroke={color} strokeWidth="10"
            strokeLinecap="round" filter="url(#glow)" />
        )}

        {/* Needle */}
        <g transform={`rotate(${angle}, ${cx}, ${cy})`}>
          <line x1={cx} y1={cy} x2={cx} y2={cy - 54}
            stroke={color} strokeWidth="2.5" strokeLinecap="round" />
          <circle cx={cx} cy={cy} r="6" fill={color} />
          <circle cx={cx} cy={cy} r="3" fill="var(--bg-card)" />
        </g>

        {/* Score */}
        <text x={cx} y={cy + 26} textAnchor="middle" fill="var(--text-primary)"
          fontSize="28" fontWeight="700" fontFamily="JetBrains Mono, monospace">
          {pct}%
        </text>

        {/* Min/Max labels */}
        <text x="28"  y="145" fill="var(--text-muted)" fontSize="9" textAnchor="middle">0%</text>
        <text x="172" y="145" fill="var(--text-muted)" fontSize="9" textAnchor="middle">100%</text>
      </svg>

      {/* Risk label badge */}
      <span style={{
        fontSize: 11, fontWeight: 700, letterSpacing: '1.5px', color,
        padding: '4px 14px', borderRadius: 20,
        background: `${color}18`, border: `1px solid ${color}40`,
      }}>
        {getLabel()}
      </span>
    </div>
  );
}

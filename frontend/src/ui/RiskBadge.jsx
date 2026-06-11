const toneClasses = {
  critical: 'bg-red-50 text-red-700 ring-red-200',
  high: 'bg-orange-50 text-orange-700 ring-orange-200',
  low: 'bg-emerald-50 text-emerald-700 ring-emerald-200',
  vip: 'bg-amber-50 text-amber-700 ring-amber-200',
  legal: 'bg-purple-50 text-purple-700 ring-purple-200',
  compliance: 'bg-blue-50 text-blue-700 ring-blue-200',
  security: 'bg-cyan-50 text-cyan-700 ring-cyan-200',
  ai: 'bg-teal-50 text-teal-700 ring-teal-200',
  human: 'bg-slate-100 text-slate-700 ring-slate-200',
};

const icons = {
  critical: '●',
  high: '▲',
  low: '●',
  vip: '★',
  legal: '⚖',
  compliance: '🔒',
  security: '🛡',
  ai: '🤖',
  human: '👤',
};

export default function RiskBadge({ label, tone = 'human' }) {
  const key = tone.toLowerCase();
  return (
    <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1 text-xs font-semibold ring-1 ${toneClasses[key] || toneClasses.human}`}>
      <span>{icons[key] || '•'}</span>
      {label}
    </span>
  );
}

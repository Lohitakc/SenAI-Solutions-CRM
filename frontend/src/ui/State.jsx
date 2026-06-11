export function LoadingState({ label = 'Loading' }) {
  return <div className="rounded border border-slate-200 bg-white p-6 text-sm text-slate-500">{label}...</div>;
}

export function ErrorState({ message }) {
  return <div className="rounded border border-red-200 bg-red-50 p-4 text-sm text-red-700">{message}</div>;
}

export function EmptyState({ message }) {
  return <div className="rounded border border-slate-200 bg-white p-6 text-sm text-slate-500">{message}</div>;
}

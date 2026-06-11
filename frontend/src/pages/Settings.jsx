import PageHeader from '../ui/PageHeader.jsx';

export default function Settings() {
  return <><PageHeader title="Settings" subtitle="Runtime configuration overview" /><div className="rounded border border-slate-200 bg-white p-5 text-sm"><p>Backend API: {import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8002'}</p><p>LLM provider is configured server-side through environment variables.</p><p>Secrets are never stored in the frontend.</p></div></>;
}

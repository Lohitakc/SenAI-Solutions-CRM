import { useState } from 'react';
import { crmApi } from '../api/crmApi.js';
import PageHeader from '../ui/PageHeader.jsx';
import { ErrorState } from '../ui/State.jsx';

export default function AIAnalysis() {
  const [form, setForm] = useState({ sender: 'customer@example.com', subject: 'Urgent refund request', body: 'This is urgent. I need a refund and may escalate legally.' });
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  async function submit() {
    setError('');
    try { setResult(await crmApi.analyze({ ...form, thread_history: [] })); } catch (err) { setError(err.message); }
  }
  return <><PageHeader title="AI Analysis" subtitle="Classify, retrieve context, draft reply, and plan recommendations" /><div className="grid gap-4 lg:grid-cols-2"><div className="rounded border border-slate-200 bg-white p-4 space-y-3"><input className="w-full rounded border p-2" value={form.sender} onChange={(e) => setForm({ ...form, sender: e.target.value })} /><input className="w-full rounded border p-2" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} /><textarea className="h-40 w-full rounded border p-2" value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} /><button onClick={submit} className="rounded bg-teal-600 px-3 py-2 text-sm text-white">Analyze</button>{error && <ErrorState message={error} />}</div><pre className="overflow-auto rounded border border-slate-200 bg-white p-4 text-xs">{result ? JSON.stringify(result, null, 2) : 'No analysis yet.'}</pre></div></>;
}

import { Link } from 'react-router-dom';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import PageHeader from '../ui/PageHeader.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';
import { useState } from 'react';

export default function Inbox() {
  const [search, setSearch] = useState('');
  const [priority, setPriority] = useState('');
  const { data, loading, error, reload } = useAsync(() => crmApi.inbox({ search: search || undefined, priority: priority || undefined, limit: 50 }), [search, priority]);
  return (
    <>
      <PageHeader title="Inbox" subtitle="Ingested customer email queue" action={<button onClick={reload} className="rounded bg-teal-600 px-3 py-2 text-sm text-white">Refresh</button>} />
      <div className="mb-4 flex flex-col gap-3 rounded border border-slate-200 bg-white p-3 md:flex-row">
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search sender, subject, body" className="rounded border border-slate-300 px-3 py-2 text-sm md:flex-1" />
        <select value={priority} onChange={(e) => setPriority(e.target.value)} className="rounded border border-slate-300 px-3 py-2 text-sm">
          <option value="">All priorities</option><option>LOW</option><option>MEDIUM</option><option>HIGH</option><option>CRITICAL</option>
        </select>
      </div>
      {loading && <LoadingState label="Loading inbox" />}
      {error && <ErrorState message={error} />}
      {!loading && data?.length === 0 && <EmptyState message="No emails match the current filters." />}
      {data?.length > 0 && (
        <div className="overflow-hidden rounded border border-slate-200 bg-white">
          <table className="min-w-full text-left text-sm">
            <thead className="bg-slate-100 text-xs uppercase text-slate-500"><tr><th className="p-3">Sender</th><th className="p-3">Subject</th><th className="p-3">Priority</th><th className="p-3">Status</th><th className="p-3">Category</th><th className="p-3">Received</th></tr></thead>
            <tbody>{data.map((email) => (
              <tr key={email.id} className="border-t border-slate-100 hover:bg-slate-50">
                <td className="p-3">{email.sender}</td>
                <td className="p-3"><Link className="font-medium text-teal-700" to={`/threads/${email.thread_id}`}>{email.subject || 'No subject'}</Link></td>
                <td className="p-3">{email.priority}</td><td className="p-3">{email.status}</td><td className="p-3">{email.category || 'Unclassified'}</td><td className="p-3">{new Date(email.received_at).toLocaleString()}</td>
              </tr>
            ))}</tbody>
          </table>
        </div>
      )}
    </>
  );
}

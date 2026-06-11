import { useParams } from 'react-router-dom';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import PageHeader from '../ui/PageHeader.jsx';
import { ErrorState, LoadingState } from '../ui/State.jsx';

export default function ThreadView() {
  const { threadId } = useParams();
  const { data, loading, error, reload } = useAsync(() => crmApi.thread(threadId), [threadId]);
  const latest = data?.emails?.at(-1);
  async function refreshAi() {
    if (!latest) return;
    await crmApi.analyze({ sender: latest.sender, subject: latest.subject, body: latest.body, email_id: latest.id, thread_history: data.emails.map((email) => email.body) });
    reload();
  }
  if (loading) return <LoadingState label="Loading thread" />;
  if (error) return <ErrorState message={error} />;
  return (
    <>
      <PageHeader title={`Thread ${data.thread_identifier}`} subtitle={`${data.status} · ${data.priority}`} action={<div className="flex gap-2"><button onClick={refreshAi} className="rounded bg-teal-600 px-3 py-2 text-sm text-white">Refresh AI</button><button onClick={() => crmApi.escalateThread(data.id).then(reload)} className="rounded bg-red-600 px-3 py-2 text-sm text-white">Escalate</button></div>} />
      <div className="grid gap-4 lg:grid-cols-[1.5fr_1fr]">
        <section className="space-y-3">{data.emails.map((email) => <article key={email.id} className="rounded border border-slate-200 bg-white p-4"><p className="text-sm font-medium">{email.sender}</p><h2 className="mt-1 font-semibold">{email.subject}</h2><p className="mt-3 whitespace-pre-wrap text-sm text-slate-700">{email.body}</p></article>)}</section>
        <aside className="space-y-4">
          <Panel title="AI Summary">{latest?.classification?.summary || 'Run AI analysis to generate a summary.'}</Panel>
          <Panel title="Classification">{latest?.classification ? `${latest.classification.category} · ${latest.classification.urgency || 'No urgency'} · ${latest.classification.confidence}` : 'Not classified'}</Panel>
          <Panel title="Reply Draft"><p className="whitespace-pre-wrap">{latest?.classification?.reply_draft || 'No reply draft yet.'}</p>{latest && <button onClick={() => crmApi.approveReply(latest.id)} className="mt-3 rounded bg-slate-900 px-3 py-2 text-sm text-white">Approve Reply</button>}</Panel>
        </aside>
      </div>
    </>
  );
}

function Panel({ title, children }) {
  return <div className="rounded border border-slate-200 bg-white p-4"><h2 className="mb-2 text-sm font-semibold">{title}</h2><div className="text-sm text-slate-700">{children}</div></div>;
}

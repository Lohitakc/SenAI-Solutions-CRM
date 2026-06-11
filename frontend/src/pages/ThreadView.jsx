import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import AgentInspector from '../ui/AgentInspector.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import RiskBadge from '../ui/RiskBadge.jsx';
import { ErrorState, LoadingState } from '../ui/State.jsx';

export default function ThreadView() {
  const { threadId } = useParams();
  const { data, loading, error, reload } = useAsync(() => crmApi.thread(threadId), [threadId]);
  const [analysis, setAnalysis] = useState(null);
  const latest = data?.emails?.at(-1);

  async function refreshAi(email = latest) {
    if (!email) return;
    const response = await crmApi.analyze({
      sender: email.sender,
      subject: email.subject,
      body: email.body,
      email_id: email.id,
      thread_history: data.emails.filter((item) => item.id !== email.id).map((item) => item.body),
      dry_run: true,
    });
    setAnalysis(response);
    reload();
  }

  if (loading) return <LoadingState label="Loading thread" />;
  if (error) return <ErrorState message={error} />;

  return (
    <>
      <PageHeader
        title={`Thread ${data.thread_identifier}`}
        subtitle={`${data.status} · ${data.priority}`}
        action={<div className="flex gap-2"><button onClick={() => refreshAi()} className="rounded bg-teal-600 px-3 py-2 text-sm text-white">Refresh AI</button><button onClick={() => crmApi.escalateThread(data.id).then(reload)} className="rounded bg-red-600 px-3 py-2 text-sm text-white">Escalate</button></div>}
      />
      <div className="grid gap-4 lg:grid-cols-[1.5fr_1fr]">
        <section className="relative space-y-4 before:absolute before:bottom-0 before:left-5 before:top-0 before:w-px before:bg-slate-200">
          {data.emails.map((email) => <TimelineMessage key={email.id} email={email} onAnalyze={() => refreshAi(email)} />)}
        </section>
        <aside className="space-y-4">
          <Panel title="AI Summary">{latest?.classification?.summary || 'Run AI analysis to generate a summary.'}</Panel>
          <Panel title="Classification">
            {latest?.classification ? <div className="flex flex-wrap gap-2"><RiskBadge label={latest.classification.category} tone={badgeTone(latest.classification.category)} /><RiskBadge label={latest.classification.urgency || 'No urgency'} tone={latest.classification.urgency === 'CRITICAL' ? 'critical' : 'high'} /><RiskBadge label={latest.classification.human_required ? 'Human Review' : 'AI Draft'} tone={latest.classification.human_required ? 'human' : 'ai'} /></div> : 'Not classified'}
          </Panel>
          <Panel title="Reply Draft">
            <p className="whitespace-pre-wrap">{latest?.classification?.reply_draft || 'No reply draft yet.'}</p>
            {latest && <button onClick={() => crmApi.approveReply(latest.id)} className="mt-3 rounded bg-slate-900 px-3 py-2 text-sm text-white">Approve Reply</button>}
          </Panel>
          <AgentInspector result={analysis} query={latest ? `${latest.subject}\n${latest.body}` : ''} threadHistory={data.emails.map((email) => email.body)} />
        </aside>
      </div>
    </>
  );
}

function TimelineMessage({ email, onAnalyze }) {
  const classification = email.classification;
  return (
    <article className="relative ml-10 rounded border border-slate-200 bg-white p-4 shadow-sm">
      <span className="absolute -left-10 top-5 grid h-10 w-10 place-items-center rounded-full border border-teal-200 bg-teal-50 text-xs font-semibold text-teal-700">AI</span>
      <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-medium">{email.sender}</p>
          <h2 className="mt-1 font-semibold text-slate-950">{email.subject || 'No subject'}</h2>
          <p className="text-xs text-slate-500">{new Date(email.received_at).toLocaleString()}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {classification?.sentiment && <RiskBadge label={classification.sentiment} tone={classification.sentiment === 'NEGATIVE' ? 'high' : 'low'} />}
          {classification?.category && <RiskBadge label={classification.category} tone={badgeTone(classification.category)} />}
          {classification?.human_required && <RiskBadge label="Escalated" tone="human" />}
        </div>
      </div>
      <p className="mt-3 whitespace-pre-wrap text-sm text-slate-700">{email.body}</p>
      {classification && (
        <details className="mt-3 rounded bg-slate-50 p-3 text-sm">
          <summary className="cursor-pointer font-medium">View AI classification</summary>
          <p className="mt-2">Urgency: {classification.urgency || 'None'} · Confidence: {Math.round((classification.confidence || 0) * 100)}%</p>
          <p className="mt-2">{classification.summary || 'No summary available.'}</p>
        </details>
      )}
      <button onClick={onAnalyze} className="mt-3 rounded border border-slate-300 px-3 py-1.5 text-xs font-medium text-slate-700 hover:bg-slate-50">Inspect this message</button>
    </article>
  );
}

function Panel({ title, children }) {
  return <div className="rounded border border-slate-200 bg-white p-4 shadow-sm"><h2 className="mb-2 text-sm font-semibold">{title}</h2><div className="text-sm text-slate-700">{children}</div></div>;
}

function badgeTone(category = '') {
  const normalized = category.toLowerCase();
  if (normalized.includes('legal')) return 'legal';
  if (normalized.includes('compliance')) return 'compliance';
  if (normalized.includes('security')) return 'security';
  if (normalized.includes('critical')) return 'critical';
  return 'ai';
}

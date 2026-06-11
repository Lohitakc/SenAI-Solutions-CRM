import { useState } from 'react';
import { crmApi } from '../api/crmApi.js';
import AgentInspector, { parseReasoning } from '../ui/AgentInspector.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import RiskBadge from '../ui/RiskBadge.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';

export default function AIAnalysis() {
  const [form, setForm] = useState({ sender: 'customer@example.com', subject: 'Urgent refund request', body: 'This is urgent. I need a refund and may escalate legally.' });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function submit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      setResult(await crmApi.analyze({ ...form, thread_history: [], dry_run: true }));
    } catch (err) {
      setError(err.message || 'AI analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <PageHeader title="AI Analysis Workspace" subtitle="Policy-grounded classification, reply drafting, and agent recommendations" />
      <div className="grid gap-5 xl:grid-cols-[0.8fr_1.2fr]">
        <form onSubmit={submit} className="space-y-3 rounded border border-slate-200 bg-white p-4 shadow-sm">
          <Field label="Sender"><input className="w-full rounded border border-slate-300 p-2 text-sm" value={form.sender} onChange={(event) => setForm({ ...form, sender: event.target.value })} /></Field>
          <Field label="Subject"><input className="w-full rounded border border-slate-300 p-2 text-sm" value={form.subject} onChange={(event) => setForm({ ...form, subject: event.target.value })} /></Field>
          <Field label="Email Body"><textarea className="h-44 w-full rounded border border-slate-300 p-2 text-sm" value={form.body} onChange={(event) => setForm({ ...form, body: event.target.value })} /></Field>
          <button type="submit" className="rounded bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700">Analyze Email</button>
          {error && <ErrorState message={error} />}
        </form>
        <AnalysisWorkspace result={result} loading={loading} query={`${form.subject}\n${form.body}`} />
      </div>
    </>
  );
}

function AnalysisWorkspace({ result, loading, query }) {
  if (loading) return <LoadingState label="Running policy-grounded AI analysis" />;
  if (!result) return <EmptyState message="Submit an email to generate an AI workspace." />;

  const classification = result.classification || {};
  const reasoning = parseReasoning(result.reasoning);
  const retrieved = classification.retrieved_chunks || [];
  const confidence = Math.round((classification.confidence || 0) * 100);
  const confidenceLabel = confidence >= 80 ? 'High Confidence' : confidence >= 55 ? 'Medium Confidence' : 'Low Confidence';
  const legalReview = hasRisk(result, ['legal', 'lawsuit']);
  const complianceReview = hasRisk(result, ['compliance', 'gdpr']);
  const securityReview = hasRisk(result, ['security', 'ransomware', 'breach']);

  return (
    <div className="space-y-4">
      <Section title="AI Summary" defaultOpen>
        <p className="text-sm leading-6 text-slate-700">{classification.summary || reasoning.summary || 'The AI generated a recommendation for this customer message.'}</p>
        <p className="mt-3 text-sm text-slate-600">Business context: {businessContext(reasoning)}</p>
        <CitationStrip chunks={retrieved} />
        <p className="mt-3 rounded bg-teal-50 p-3 text-sm font-medium text-teal-800">Overall recommendation: {result.escalation_required ? 'Route to a human owner before any customer response.' : 'Review the draft and proceed through the normal support workflow.'}</p>
      </Section>

      <div className="grid gap-4 lg:grid-cols-2">
        <Section title="Classification" defaultOpen>
          <div className="flex flex-wrap gap-2">
            <RiskBadge label={classification.category || 'Unclassified'} tone={badgeTone(classification.category)} />
            <RiskBadge label={classification.urgency || 'No urgency'} tone={classification.urgency === 'CRITICAL' ? 'critical' : 'high'} />
            <RiskBadge label={classification.sentiment || 'Neutral'} tone="ai" />
            <RiskBadge label={classification.human_required ? 'Human review required' : 'AI draft ready'} tone={classification.human_required ? 'human' : 'ai'} />
          </div>
        </Section>
        <Section title="AI Confidence Panel" defaultOpen>
          <div className="h-3 rounded-full bg-slate-100"><div className={`h-3 rounded-full ${confidence >= 80 ? 'bg-emerald-500' : confidence >= 55 ? 'bg-amber-500' : 'bg-red-500'}`} style={{ width: `${confidence}%` }} /></div>
          <p className="mt-2 text-sm font-semibold">{confidence}% · {confidenceLabel}</p>
          {confidence < 55 && <p className="mt-2 text-sm text-red-700">Manual review recommended due to low confidence.</p>}
        </Section>
      </div>

      <Section title="Retrieved Policies" defaultOpen>
        <div className="space-y-3">
          {retrieved.map((chunk, index) => <PolicyCard key={chunk.embedding_reference || index} chunk={chunk} />)}
          {!retrieved.length && <EmptyState message="No retrieved policies returned." />}
        </div>
      </Section>

      <Section title="Suggested Reply" defaultOpen>
        <div className="rounded border border-slate-200 bg-slate-50 p-4">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Formatted email preview</p>
            <button onClick={() => navigator.clipboard?.writeText(classification.reply_draft || '')} className="rounded border border-slate-300 px-3 py-1 text-xs text-slate-700">Copy</button>
          </div>
          <div className="space-y-2 text-sm leading-6 text-slate-800">{renderMarkdownLite(classification.reply_draft || 'No draft generated.')}</div>
          <CitationStrip chunks={retrieved} />
        </div>
      </Section>

      <Section title="Execution Plan" defaultOpen>
        <ul className="space-y-2">{(result.execution_plan || []).map((item, index) => <li key={index} className="flex gap-2 rounded bg-slate-50 p-3 text-sm"><span className="text-emerald-600">✓</span><span>{item}</span></li>)}</ul>
      </Section>

      <Section title="Escalation Panel" defaultOpen>
        <div className="flex flex-wrap gap-2">
          <RiskBadge label={`Escalation ${result.escalation_required ? 'required' : 'not required'}`} tone={result.escalation_required ? 'critical' : 'low'} />
          <RiskBadge label={`Legal review ${legalReview ? 'required' : 'not required'}`} tone={legalReview ? 'legal' : 'low'} />
          <RiskBadge label={`Human approval ${result.escalation_required ? 'required' : 'optional'}`} tone={result.escalation_required ? 'human' : 'ai'} />
          <RiskBadge label={`Compliance review ${complianceReview ? 'required' : 'not required'}`} tone={complianceReview ? 'compliance' : 'low'} />
          <RiskBadge label={`Security review ${securityReview ? 'required' : 'not required'}`} tone={securityReview ? 'security' : 'low'} />
        </div>
      </Section>

      <Section title="Context Used">
        <div className="grid gap-2 sm:grid-cols-2">
          <ContextItem label="Thread history included" active />
          <ContextItem label="CRM profile used" active={Boolean(reasoning.customer)} />
          <ContextItem label="Account status used" active={Boolean(reasoning.account)} />
          <ContextItem label="Retrieved policies used" active={retrieved.length > 0} />
        </div>
      </Section>

      <AgentInspector result={result} query={query} defaultOpen />
    </div>
  );
}

function Field({ label, children }) {
  return <label className="block"><span className="mb-1 block text-xs font-semibold uppercase tracking-wide text-slate-500">{label}</span>{children}</label>;
}

function Section({ title, children, defaultOpen = false }) {
  return <details className="rounded border border-slate-200 bg-white p-4 shadow-sm transition-all" open={defaultOpen}><summary className="cursor-pointer text-sm font-semibold text-slate-950">{title}</summary><div className="mt-4">{children}</div></details>;
}

function PolicyCard({ chunk }) {
  return <details className="rounded border border-slate-200 p-3" open><summary className="cursor-pointer text-sm font-medium">{chunk.title || 'Policy'} <span className="text-xs text-slate-500">· {chunk.source_file} · {(chunk.score * 100).toFixed(1)}%</span></summary><p className="mt-3 text-sm leading-6 text-slate-700">{chunk.content}</p></details>;
}

function CitationStrip({ chunks }) {
  const sources = [...new Set((chunks || []).map((chunk) => chunk.source_file).filter(Boolean))];
  if (!sources.length) return null;
  return <div className="mt-3 flex flex-wrap gap-2 text-xs"><span className="font-semibold text-slate-500">Based on:</span>{sources.map((source) => <RiskBadge key={source} label={source} tone="ai" />)}</div>;
}

function ContextItem({ label, active }) {
  return <div className="rounded bg-slate-50 p-3 text-sm"><span className={active ? 'text-emerald-600' : 'text-slate-400'}>{active ? '✓' : '○'}</span> {label}</div>;
}

function renderMarkdownLite(text) {
  return text.split('\n').map((line, index) => <p key={index} className={line.startsWith('- ') ? 'pl-4' : ''}>{line}</p>);
}

function businessContext(reasoning) {
  const customer = reasoning.customer || {};
  const account = reasoning.account || {};
  return `VIP ${customer.vip ? 'yes' : 'no'}, churn risk ${customer.churn_risk || 'unknown'}, account plan ${account.plan || 'unknown'}.`;
}

function hasRisk(result, terms) {
  const text = `${result.status || ''} ${result.reasoning || ''} ${result.execution_plan?.join(' ') || ''} ${result.classification?.category || ''}`.toLowerCase();
  return terms.some((term) => text.includes(term.toLowerCase()));
}

function badgeTone(category = '') {
  const normalized = category.toLowerCase();
  if (normalized.includes('legal')) return 'legal';
  if (normalized.includes('compliance')) return 'compliance';
  if (normalized.includes('security')) return 'security';
  if (normalized.includes('critical')) return 'critical';
  return 'ai';
}

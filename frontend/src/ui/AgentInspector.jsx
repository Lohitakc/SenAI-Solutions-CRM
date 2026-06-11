import { EmptyState } from './State.jsx';
import RiskBadge from './RiskBadge.jsx';

export default function AgentInspector({ result, query, threadHistory = [], defaultOpen = false }) {
  if (!result) return <EmptyState message="Run AI analysis to inspect the agent reasoning pipeline." />;
  const classification = result.classification || {};
  const reasoning = parseReasoning(result.reasoning);
  const retrieved = classification.retrieved_chunks || [];
  const confidence = Math.round((classification.confidence || 0) * 100);

  return (
    <details className="rounded border border-slate-200 bg-white p-4 shadow-sm" open={defaultOpen}>
      <summary className="cursor-pointer text-sm font-semibold text-slate-950">AI Agent Inspector</summary>
      <div className="mt-4 space-y-4">
        <InspectorBlock title="User Query">
          <p className="text-sm text-slate-700">{query || classification.summary || 'No query captured.'}</p>
        </InspectorBlock>
        <div className="grid gap-3 md:grid-cols-2">
          <InspectorBlock title="Thread History Used">
            <p>{threadHistory.length || reasoning.prompt_metadata?.thread_history_count || 0} messages included</p>
          </InspectorBlock>
          <InspectorBlock title="CRM Context Used">
            <p>VIP: {reasoning.customer?.vip ? 'Yes' : 'No'} · Churn: {reasoning.customer?.churn_risk || 'unknown'} · Plan: {reasoning.account?.plan || 'unknown'}</p>
          </InspectorBlock>
          <InspectorBlock title="Confidence Score">
            <div className="h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-teal-500" style={{ width: `${confidence}%` }} /></div>
            <p className="mt-2">{confidence}%</p>
          </InspectorBlock>
          <InspectorBlock title="Escalation Decision">
            <RiskBadge label={result.escalation_required ? 'Human review required' : 'No escalation required'} tone={result.escalation_required ? 'human' : 'low'} />
          </InspectorBlock>
        </div>
        <InspectorBlock title="Knowledge Documents Retrieved">
          <div className="flex flex-wrap gap-2">
            {retrieved.length ? retrieved.map((chunk, index) => <RiskBadge key={chunk.embedding_reference || index} label={chunk.source_file || 'Policy'} tone="ai" />) : <span>No policies retrieved</span>}
          </div>
        </InspectorBlock>
        <InspectorBlock title="Tool Calls Executed">
          <div className="flex flex-wrap gap-2">
            {(reasoning.trace || []).map((step, index) => <RiskBadge key={index} label={step.Action || 'tool'} tone="security" />)}
          </div>
        </InspectorBlock>
        <InspectorBlock title="Reasoning Timeline">
          <ReasoningTimeline trace={reasoning.trace || []} />
        </InspectorBlock>
        <InspectorBlock title="Final Recommendation">
          <p>{result.escalation_required ? 'Require human approval before external response.' : 'Review the AI draft and continue standard workflow.'}</p>
        </InspectorBlock>
      </div>
    </details>
  );
}

export function parseReasoning(reasoning) {
  try {
    return JSON.parse(reasoning || '{}');
  } catch {
    return { summary: reasoning };
  }
}

function InspectorBlock({ title, children }) {
  return <section className="rounded bg-slate-50 p-3 text-sm text-slate-700"><h3 className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-500">{title}</h3>{children}</section>;
}

function ReasoningTimeline({ trace }) {
  if (!trace.length) return <EmptyState message="No structured reasoning trace available." />;
  return (
    <div className="space-y-3">
      {trace.map((step, index) => (
        <div key={index} className="rounded border border-slate-200 bg-white p-3">
          <p><strong>Thought:</strong> {step.Thought}</p>
          <p className="text-slate-400">↓</p>
          <p><strong>Action:</strong> {step.Action}</p>
          <p className="text-slate-400">↓</p>
          <p><strong>Observation:</strong> {step.Observation}</p>
          <p className="text-slate-400">↓</p>
          <p><strong>Decision:</strong> {step['Next Thought']}</p>
        </div>
      ))}
    </div>
  );
}

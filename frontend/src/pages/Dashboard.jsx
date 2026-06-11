import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import MetricCard from '../ui/MetricCard.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import RiskBadge from '../ui/RiskBadge.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';

const colors = ['#0f766e', '#2563eb', '#c2410c', '#7c3aed', '#475569'];

export default function Dashboard() {
  const { data, loading, error } = useAsync(() => crmApi.dashboard(), []);
  if (loading) return <LoadingState label="Loading dashboard" />;
  if (error) return <ErrorState message={error} />;
  if (!data) return <EmptyState message="No dashboard data available." />;

  return (
    <>
      <PageHeader title="Dashboard" subtitle="Live CRM operations and executive AI command center" />
      <section className="mb-6 rounded border border-slate-200 bg-white p-5 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-950">Executive Command Center</h2>
        <div className="mt-4 grid gap-3 md:grid-cols-4">
          <CommandCard label="Critical Emails Awaiting Review" value={data.critical_queue?.length || 0} tone="critical" />
          <CommandCard label="VIP Customers Requiring Attention" value={data.vip_customers || 0} tone="vip" />
          <CommandCard label="High Churn Risk Accounts" value={data.at_risk_accounts?.length || 0} tone="high" />
          <CommandCard label="AI Auto-Resolved Today" value={Math.max((data.total_emails || 0) - (data.pending_approvals || 0), 0)} tone="ai" />
          <CommandCard label="Human Escalations Today" value={data.escalations} tone="human" />
          <CommandCard label="Most Retrieved Policy" value={data.most_retrieved_policy || 'Pending'} tone="ai" />
          <CommandCard label="Average AI Confidence" value={data.agent_confidence} tone="low" />
          <CommandCard label="Pending Human Approvals" value={data.pending_approvals || 0} tone="human" />
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-4">
        <MetricCard label="Total Emails" value={data.total_emails} />
        <MetricCard label="Open Threads" value={data.open_threads} />
        <MetricCard label="Escalations" value={data.escalations} />
        <MetricCard label="Avg Response Time" value={data.average_response_time} />
        <MetricCard label="Human Intervention" value={`${data.human_intervention_rate}%`} />
        <MetricCard label="Escalation Rate" value={`${data.escalation_rate}%`} />
        <MetricCard label="Agent Confidence" value={data.agent_confidence} />
        <MetricCard label="Critical Queue" value={data.critical_queue?.length || 0} />
        <MetricCard label="VIP Customers" value={data.vip_customers || 0} />
        <MetricCard label="Pending Approvals" value={data.pending_approvals || 0} />
        <MetricCard label="Knowledge Chunks" value={data.knowledge_retrieval_count || 0} />
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <ChartCard title="Top Categories"><PieBlock data={data.category_distribution} /></ChartCard>
        <ChartCard title="Priority Distribution"><BarBlock data={data.priority_distribution} /></ChartCard>
      </section>

      <section className="mt-6 grid gap-4 lg:grid-cols-3">
        <ListCard title="Critical Queue" items={data.critical_queue || []} empty="No critical alerts.">
          {(item) => <><span className="font-medium">{item.subject || 'No subject'}</span><span className="ml-2 text-slate-500">{item.priority} · {item.category || 'Unclassified'}</span></>}
        </ListCard>
        <ListCard title="At-Risk Customers" items={data.at_risk_accounts || []} empty="No at-risk accounts.">
          {(item) => <><span className="font-medium">{item.domain}</span><span className="ml-2 text-slate-500">{item.risk_events} risk events</span>{item.vip && <span className="ml-2"><RiskBadge label="VIP" tone="vip" /></span>}</>}
        </ListCard>
        <ListCard title="Recent Activity" items={data.recent_activity || []} empty="No recent activity yet.">
          {(item) => <><span className="font-medium">{item.event}</span><span className="ml-2 text-slate-500">{item.details}</span></>}
        </ListCard>
      </section>
    </>
  );
}

function CommandCard({ label, value, tone }) {
  return <div className="rounded bg-slate-50 p-3"><RiskBadge label={label} tone={tone} /><p className="mt-3 break-words text-lg font-semibold text-slate-950">{value}</p></div>;
}

function ChartCard({ title, children }) {
  return <div className="h-80 rounded border border-slate-200 bg-white p-4 shadow-sm"><h2 className="text-sm font-semibold">{title}</h2>{children}</div>;
}

function ListCard({ title, items, empty, children }) {
  return <div className="rounded border border-slate-200 bg-white p-4 shadow-sm"><h2 className="text-sm font-semibold text-slate-900">{title}</h2><div className="mt-3 space-y-2">{items.length ? items.map((item, index) => <div key={item.id || item.domain || index} className="rounded bg-slate-50 p-3 text-sm">{children(item)}</div>) : <EmptyState message={empty} />}</div></div>;
}

function PieBlock({ data }) {
  return <ResponsiveContainer width="100%" height="90%"><PieChart><Pie data={data} dataKey="value" nameKey="name" outerRadius={90}>{data.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer>;
}

function BarBlock({ data }) {
  return <ResponsiveContainer width="100%" height="90%"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#0f766e" /></BarChart></ResponsiveContainer>;
}

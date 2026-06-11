import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import MetricCard from '../ui/MetricCard.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';

const colors = ['#0f766e', '#2563eb', '#c2410c', '#7c3aed', '#475569'];

export default function Dashboard() {
  const { data, loading, error } = useAsync(() => crmApi.dashboard(), []);
  if (loading) return <LoadingState label="Loading dashboard" />;
  if (error) return <ErrorState message={error} />;
  if (!data) return <EmptyState message="No dashboard data available." />;
  return (
    <>
      <PageHeader title="Dashboard" subtitle="Live CRM operations overview" />
      <section className="grid gap-4 md:grid-cols-4">
        <MetricCard label="Total Emails" value={data.total_emails} />
        <MetricCard label="Open Threads" value={data.open_threads} />
        <MetricCard label="Escalations" value={data.escalations} />
        <MetricCard label="Avg Response Time" value={data.average_response_time} />
      </section>
      <section className="mt-6 grid gap-4 lg:grid-cols-2">
        <ChartCard title="Category Distribution"><PieBlock data={data.category_distribution} /></ChartCard>
        <ChartCard title="Priority Distribution"><BarBlock data={data.priority_distribution} /></ChartCard>
      </section>
      <section className="mt-6 rounded border border-slate-200 bg-white p-4">
        <h2 className="text-sm font-semibold text-slate-900">Recent Activity</h2>
        <div className="mt-3 space-y-2">
          {data.recent_activity.length ? data.recent_activity.map((item) => (
            <div key={item.id} className="rounded bg-slate-50 p-3 text-sm">
              <span className="font-medium">{item.event}</span>
              <span className="ml-2 text-slate-500">{item.details}</span>
            </div>
          )) : <EmptyState message="No recent activity yet." />}
        </div>
      </section>
    </>
  );
}

function ChartCard({ title, children }) {
  return <div className="h-80 rounded border border-slate-200 bg-white p-4"><h2 className="text-sm font-semibold">{title}</h2>{children}</div>;
}

function PieBlock({ data }) {
  return <ResponsiveContainer width="100%" height="90%"><PieChart><Pie data={data} dataKey="value" nameKey="name" outerRadius={90}>{data.map((_, index) => <Cell key={index} fill={colors[index % colors.length]} />)}</Pie><Tooltip /></PieChart></ResponsiveContainer>;
}

function BarBlock({ data }) {
  return <ResponsiveContainer width="100%" height="90%"><BarChart data={data}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#0f766e" /></BarChart></ResponsiveContainer>;
}

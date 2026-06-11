import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import PageHeader from '../ui/PageHeader.jsx';
import { ErrorState, LoadingState } from '../ui/State.jsx';

export default function Analytics() {
  const { data, loading, error } = useAsync(() => crmApi.dashboard(), []);
  if (loading) return <LoadingState label="Loading analytics" />;
  if (error) return <ErrorState message={error} />;
  return <><PageHeader title="Analytics" subtitle="Operational trends and AI intervention metrics" /><div className="grid gap-4 lg:grid-cols-2"><Chart title="Daily Volume"><LineChart data={data.daily_volume}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Line dataKey="value" stroke="#0f766e" /></LineChart></Chart><Chart title="Sentiment"><BarChart data={data.sentiment_distribution}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#2563eb" /></BarChart></Chart><Chart title="Categories"><BarChart data={data.category_distribution}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#c2410c" /></BarChart></Chart><Chart title="Priorities"><BarChart data={data.priority_distribution}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#7c3aed" /></BarChart></Chart></div><div className="mt-4 rounded border bg-white p-4 text-sm">Human intervention rate: {data.human_intervention_rate}%</div></>;
}

function Chart({ title, children }) {
  return <div className="h-80 rounded border border-slate-200 bg-white p-4"><h2 className="mb-2 text-sm font-semibold">{title}</h2><ResponsiveContainer width="100%" height="90%">{children}</ResponsiveContainer></div>;
}

import { Link, useParams } from 'react-router-dom';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import MetricCard from '../ui/MetricCard.jsx';
import PageHeader from '../ui/PageHeader.jsx';
import RiskBadge from '../ui/RiskBadge.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';

export default function CustomerView() {
  const { contactId } = useParams();
  return contactId ? <CustomerProfile contactId={contactId} /> : <CustomerList />;
}

function CustomerList() {
  const { data, loading, error } = useAsync(() => crmApi.customers(), []);
  if (loading) return <LoadingState label="Loading customers" />;
  if (error) return <ErrorState message={error} />;
  if (!data?.length) return <EmptyState message="No customers found. Replay the assessment dataset to populate contacts." />;

  return (
    <>
      <PageHeader title="Customers" subtitle="Enriched CRM profiles powered by live contacts and synthetic account context" />
      <div className="grid gap-4 xl:grid-cols-2">
        {data.map((customer) => <CustomerCard key={customer.id} customer={customer} />)}
      </div>
    </>
  );
}

function CustomerCard({ customer }) {
  const profile = customer.profile || {};
  return (
    <Link to={`/customers/${customer.id}`} className="rounded border border-slate-200 bg-white p-4 shadow-sm transition hover:border-teal-300 hover:shadow-md">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="font-semibold text-slate-950">{customer.name || customer.email}</h2>
          <p className="text-sm text-slate-500">{customer.company || customer.email}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {profile.vip && <RiskBadge label="VIP" tone="vip" />}
          <RiskBadge label={`Churn ${customer.churn_prediction_score ?? 0}%`} tone={(customer.churn_prediction_score ?? 0) > 70 ? 'critical' : (customer.churn_prediction_score ?? 0) > 45 ? 'high' : 'low'} />
        </div>
      </div>
      <div className="mt-4 grid gap-3 sm:grid-cols-3">
        <MiniMetric label="Tier" value={profile.subscription_tier || 'Unknown'} />
        <MiniMetric label="Health" value={`${profile.customer_health_score ?? '—'}`} />
        <MiniMetric label="Churn" value={profile.churn_risk || 'unknown'} tone={profile.churn_risk} />
        <MiniMetric label="Value" value={formatCurrency(profile.account_value)} />
        <MiniMetric label="Renewal" value={profile.renewal_date || '—'} />
        <MiniMetric label="Tickets" value={profile.open_tickets ?? 0} />
      </div>
    </Link>
  );
}

function CustomerProfile({ contactId }) {
  const { data, loading, error } = useAsync(() => crmApi.customerProfile(contactId), [contactId]);
  if (loading) return <LoadingState label="Loading customer profile" />;
  if (error) return <ErrorState message={error} />;

  const profile = data.profile || {};
  const account = data.account_status || {};
  const churnScore = data.churn_prediction_score ?? 0;
  return (
    <>
      <PageHeader title={data.name || data.email} subtitle={`${data.company || 'Customer'} · ${profile.subscription_tier || 'Unknown tier'}`} action={profile.vip && <RiskBadge label="VIP Customer" tone="vip" />} />
      <section className="grid gap-4 md:grid-cols-5">
        <MetricCard label="Customer Health" value={profile.customer_health_score ?? '—'} />
        <MetricCard label="Churn Risk" value={profile.churn_risk || 'unknown'} />
        <MetricCard label="Churn Prediction" value={`${churnScore}%`} />
        <MetricCard label="Account Value" value={formatCurrency(profile.account_value)} />
        <MetricCard label="Open Tickets" value={profile.open_tickets ?? 0} />
      </section>
      <section className="mt-6 rounded border border-slate-200 bg-white p-4 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-950">Churn Prediction Score</h2>
        <div className="mt-3 h-3 rounded-full bg-slate-100"><div className={`h-3 rounded-full ${churnScore > 70 ? 'bg-red-500' : churnScore > 45 ? 'bg-amber-500' : 'bg-emerald-500'}`} style={{ width: `${churnScore}%` }} /></div>
        <div className="mt-3 flex flex-wrap gap-2">{(data.churn_prediction_factors || []).map((factor) => <RiskBadge key={factor} label={factor} tone={churnScore > 70 ? 'critical' : 'high'} />)}</div>
      </section>
      <section className="mt-6 grid gap-4 lg:grid-cols-[1fr_1fr]">
        <Panel title="Account Summary">
          <Info label="Email" value={data.email} />
          <Info label="Renewal Date" value={profile.renewal_date || 'Not set'} />
          <Info label="Account Manager" value={profile.assigned_account_manager || 'Unassigned'} />
          <Info label="Billing State" value={account.billing_state || 'unknown'} />
          <Info label="Plan" value={account.plan || 'unknown'} />
          <Info label="Seat Count" value={account.seat_count ?? 0} />
          <Info label="API Limits" value={account.api_limits || 'unknown'} />
        </Panel>
        <Panel title="Risk Indicators">
          <RiskBadge label={`Churn: ${profile.churn_risk || 'unknown'}`} tone={profile.churn_risk === 'critical' ? 'critical' : 'high'} />
          <RiskBadge label={`Billing: ${account.billing_state || 'unknown'}`} tone={account.billing_state === 'at_risk' ? 'critical' : 'low'} />
          <RiskBadge label={`Health: ${profile.customer_health_score ?? '—'}`} tone={(profile.customer_health_score ?? 100) < 60 ? 'high' : 'low'} />
        </Panel>
      </section>
      <section className="mt-6 grid gap-4 lg:grid-cols-3">
        <Panel title="Recent Conversations">
          <Timeline items={data.recent_conversations || []} empty="No conversations yet." render={(item) => <><p className="font-medium">{item.subject || 'No subject'}</p><p className="text-xs text-slate-500">{new Date(item.received_at).toLocaleString()} · {item.category || 'Unclassified'}</p></>} />
        </Panel>
        <Panel title="AI Analyses">
          <Timeline items={data.ai_analyses || []} empty="No AI analysis yet." render={(item) => <><p className="font-medium">{item.category}</p><p className="text-xs text-slate-500">{item.urgency || 'No urgency'} · confidence {Math.round((item.confidence || 0) * 100)}%</p></>} />
        </Panel>
        <Panel title="Recommended Actions">
          <Timeline items={data.recommended_actions || []} empty="No recommendations." render={(item) => <p>{item}</p>} />
        </Panel>
      </section>
    </>
  );
}

function MiniMetric({ label, value, tone }) {
  return <div className="rounded bg-slate-50 p-3"><p className="text-xs uppercase tracking-wide text-slate-500">{label}</p><p className={`mt-1 text-sm font-semibold ${tone === 'critical' || tone === 'high' ? 'text-red-700' : 'text-slate-900'}`}>{value}</p></div>;
}

function Panel({ title, children }) {
  return <div className="rounded border border-slate-200 bg-white p-4 shadow-sm"><h2 className="mb-3 text-sm font-semibold text-slate-950">{title}</h2><div className="space-y-3 text-sm text-slate-700">{children}</div></div>;
}

function Info({ label, value }) {
  return <div className="flex justify-between gap-3 border-b border-slate-100 pb-2"><span className="text-slate-500">{label}</span><span className="font-medium text-slate-900">{value}</span></div>;
}

function Timeline({ items, empty, render }) {
  if (!items.length) return <EmptyState message={empty} />;
  return items.map((item, index) => <div key={item.id || item.email_id || item || index} className="rounded bg-slate-50 p-3">{render(item)}</div>);
}

function formatCurrency(value = 0) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value || 0);
}

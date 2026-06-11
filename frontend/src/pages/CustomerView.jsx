import { useParams } from 'react-router-dom';
import { crmApi } from '../api/crmApi.js';
import { useAsync } from '../hooks/useAsync.js';
import PageHeader from '../ui/PageHeader.jsx';
import { ErrorState, LoadingState } from '../ui/State.jsx';

export default function CustomerView() {
  const { contactId } = useParams();
  const { data, loading, error } = useAsync(() => crmApi.contact(contactId), [contactId]);
  if (loading) return <LoadingState label="Loading customer" />;
  if (error) return <ErrorState message={error} />;
  return <><PageHeader title={data.name || data.email} subtitle="Customer profile" /><div className="rounded border border-slate-200 bg-white p-5 text-sm"><p>Email: {data.email}</p><p>Company: {data.company || 'Unknown'}</p><p>Created: {new Date(data.created_at).toLocaleString()}</p></div></>;
}

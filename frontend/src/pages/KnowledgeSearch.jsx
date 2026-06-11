import { useState } from 'react';
import { crmApi } from '../api/crmApi.js';
import PageHeader from '../ui/PageHeader.jsx';
import { EmptyState, ErrorState, LoadingState } from '../ui/State.jsx';

export default function KnowledgeSearch() {
  const [query, setQuery] = useState('refund policy');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  async function search(event) {
    event?.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError('');
    setSearched(true);
    try {
      const response = await crmApi.searchKnowledge({ query, top_k: 5, threshold: 0 });
      setResults(response.chunks || []);
    } catch (err) {
      setError(err.message || 'Knowledge search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <PageHeader title="Knowledge Base Explorer" subtitle="Search local RAG policies with ChromaDB retrieval and citations" />
      <form onSubmit={search} className="rounded border border-slate-200 bg-white p-4 shadow-sm">
        <label className="text-xs font-semibold uppercase tracking-wide text-slate-500">Search policy context</label>
        <div className="mt-2 flex flex-col gap-2 sm:flex-row">
          <input className="flex-1 rounded border border-slate-300 px-3 py-2 text-sm focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-100" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search refunds, GDPR, SLA, pricing, API limits..." />
          <button type="submit" className="rounded bg-teal-600 px-4 py-2 text-sm font-medium text-white hover:bg-teal-700">Search</button>
        </div>
      </form>

      <div className="mt-5 space-y-3">
        {loading && <LoadingState label="Retrieving knowledge" />}
        {error && <ErrorState message={error} />}
        {!loading && !error && searched && !results.length && <EmptyState message="No matching policy chunks found." />}
        {!loading && !error && !searched && <EmptyState message="Run a search to explore retrieved policy chunks." />}
        {!loading && !error && results.map((chunk, index) => (
          <details key={`${chunk.embedding_reference || index}`} className="group rounded border border-slate-200 bg-white p-4 shadow-sm" open={index === 0}>
            <summary className="cursor-pointer list-none">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h2 className="font-semibold text-slate-950">{chunk.title || 'Policy Chunk'}</h2>
                  <p className="text-xs text-slate-500">{chunk.source_file || 'Unknown source'} · similarity {(chunk.score * 100).toFixed(1)}%</p>
                </div>
                <span className="rounded-full bg-teal-50 px-3 py-1 text-xs font-medium text-teal-700">Expand</span>
              </div>
            </summary>
            <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-slate-700">{highlightMatches(chunk.content, query)}</p>
          </details>
        ))}
      </div>
    </>
  );
}

function highlightMatches(text, query) {
  const terms = query.trim().split(/\s+/).filter((term) => term.length > 2);
  if (!terms.length) return text;
  const pattern = new RegExp(`(${terms.map(escapeRegExp).join('|')})`, 'gi');
  const exactPattern = new RegExp(`^(${terms.map(escapeRegExp).join('|')})$`, 'i');
  return text.split(pattern).map((part, index) => (
    exactPattern.test(part) ? <mark key={index} className="rounded bg-amber-100 px-1 text-amber-900">{part}</mark> : part
  ));
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

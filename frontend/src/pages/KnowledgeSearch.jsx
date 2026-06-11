import { useState } from 'react';
import { crmApi } from '../api/crmApi.js';
import PageHeader from '../ui/PageHeader.jsx';

export default function KnowledgeSearch() {
  const [query, setQuery] = useState('refund policy');
  const [results, setResults] = useState([]);
  async function search() {
    const response = await crmApi.searchKnowledge({ query, top_k: 5, threshold: 0 });
    setResults(response.chunks);
  }
  return <><PageHeader title="Knowledge Search" subtitle="Search local ChromaDB knowledge chunks" /><div className="mb-4 flex gap-2"><input className="flex-1 rounded border border-slate-300 px-3 py-2" value={query} onChange={(e) => setQuery(e.target.value)} /><button onClick={search} className="rounded bg-teal-600 px-3 py-2 text-sm text-white">Search</button></div><div className="space-y-3">{results.map((chunk, index) => <article key={index} className="rounded border border-slate-200 bg-white p-4"><div className="mb-2 text-xs text-slate-500">{chunk.source_file} · score {chunk.score.toFixed(3)}</div><p className="text-sm text-slate-700">{chunk.content}</p></article>)}</div></>;
}

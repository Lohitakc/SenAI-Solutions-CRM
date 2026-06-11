import { api } from './client.js';

export const crmApi = {
  dashboard: () => api.get('/api/analytics/summary').then((res) => res.data),
  inbox: (params) => api.get('/api/emails', { params }).then((res) => res.data),
  thread: (id) => api.get(`/api/threads/${id}/detail`).then((res) => res.data),
  contact: (id) => api.get(`/api/contacts/${id}`).then((res) => res.data),
  classify: (payload) => api.post('/api/ai/classify', payload).then((res) => res.data),
  reply: (payload) => api.post('/api/ai/reply', payload).then((res) => res.data),
  searchKnowledge: (payload) => api.post('/api/rag/search', payload).then((res) => res.data),
  analyze: (payload) => api.post('/api/agent/analyze', payload).then((res) => res.data),
  history: (id) => api.get(`/api/agent/history/${id}`).then((res) => res.data),
  approveReply: (id) => api.post(`/api/emails/${id}/approve-reply`).then((res) => res.data),
  escalateThread: (id) => api.post(`/api/threads/${id}/escalate`).then((res) => res.data),
};

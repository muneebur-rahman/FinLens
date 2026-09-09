import { DashboardData, Transaction } from './types';

const API_BASE =import.meta.env.VITE_API_URL || '';

export async function uploadStatement(file: File): Promise<DashboardData> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'We couldn\'t read this statement. Please try another PDF or CSV.');
  }

  return response.json();
}

export async function loadDemoStatement(): Promise<DashboardData> {
  const response = await fetch(`${API_BASE}/demo`, {
    method: 'POST',
  });

  if (!response.ok) {
    throw new Error('Failed to load demo statement.');
  }

  return response.json();
}

export async function fetchDashboard(sessionId: string): Promise<DashboardData> {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}/dashboard`);
  if (!response.ok) {
    throw new Error('Failed to fetch dashboard data.');
  }
  return response.json();
}

export async function fetchTransactions(
  sessionId: string,
  params?: { search?: string; category?: string; type?: string; sort_by?: string; sort_order?: string }
): Promise<{ transactions: Transaction[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.category) query.append('category', params.category);
  if (params?.type) query.append('type', params.type);
  if (params?.sort_by) query.append('sort_by', params.sort_by);
  if (params?.sort_order) query.append('sort_order', params.sort_order);

  const response = await fetch(`${API_BASE}/sessions/${sessionId}/transactions?${query.toString()}`);
  if (!response.ok) {
    throw new Error('Failed to fetch transactions.');
  }
  return response.json();
}

export async function sendChatMessage(
  sessionId: string,
  message: string
): Promise<{ answer: string; data_points?: any }> {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });

  if (!response.ok) {
    throw new Error('Failed to communicate with AI Assistant.');
  }
  return response.json();
}

export async function purgeSession(sessionId: string): Promise<boolean> {
  const response = await fetch(`${API_BASE}/sessions/${sessionId}`, {
    method: 'DELETE',
  });
  return response.ok;
}

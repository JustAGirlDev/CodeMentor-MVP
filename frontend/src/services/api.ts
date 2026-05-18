/**
 * Bridge: CaptCoder frontend ↔ CodeMentor backend
 * Replaces mock services with real API calls to mentor --serve
 */

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export interface ExplainRequest {
  code: string;
  filepath?: string;
  startLine?: number;
  endLine?: number;
  mode?: 'explain' | 'analytics' | 'chart' | 'battle';
  modelA?: string;
  modelB?: string;
}

export interface ExplainResponse {
  html: string;
  metrics?: {
    total_lines: number;
    code_lines: number;
    complexity_estimate: number;
    security_flags: string[];
    functions: any[];
  };
  cached?: boolean;
  timestamp: string;
}

export interface Challenge {
  id: number;
  title: string;
  difficulty: 'tutorial' | 'medium' | 'nightmare';
  language: string;
  prompt: string;
  bounty: number;
  tags: string[];
}

export async function explainCode(req: ExplainRequest): Promise<<ExplainResponse> {
  const res = await fetch(`${API_BASE}/explain`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`Backend error: ${res.status}`);
  return res.json();
}

export async function getChallenges(difficulty?: string): Promise<<Challenge[]> {
  const url = difficulty 
    ? `${API_BASE}/challenges?difficulty=${difficulty}`
    : `${API_BASE}/challenges`;
  const res = await fetch(url);
  return res.json();
}

export async function submitBattle(
  code: string, 
  modelA: string, 
  modelB: string
): Promise<{winner: string; reasoning: string; scores: [number, number]}> {
  const res = await fetch(`${API_BASE}/battle`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code, modelA, modelB }),
  });
  return res.json();
}

export async function getLeaderboard(): Promise<Array<{user_hash: string; xp: number; level: number}>> {
  const res = await fetch(`${API_BASE}/leaderboard`);
  return res.json();
}

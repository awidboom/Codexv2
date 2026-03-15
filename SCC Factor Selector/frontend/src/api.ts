import { Ap42Section, CartItem, SccCodeMatch, SccMatch, SccSector, SearchResponse } from './types';

export async function searchFactors(params: Record<string, string>) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`/api/search?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error('Search request failed');
  }
  return (await response.json()) as SearchResponse;
}

export async function fetchSectors() {
  const response = await fetch('/api/scc/sectors');
  if (!response.ok) {
    throw new Error('Sector request failed');
  }
  return (await response.json()) as SccSector[];
}

export async function fetchAp42Sections() {
  const response = await fetch('/api/ap42/sections');
  if (!response.ok) {
    throw new Error('AP-42 sections request failed');
  }
  return (await response.json()) as Ap42Section[];
}

export async function fetchHierarchy(params: {
  level: number;
  sector?: string;
  level1?: string;
  level2?: string;
  level3?: string;
}) {
  const searchParams = new URLSearchParams();
  searchParams.set('level', params.level.toString());
  if (params.sector) searchParams.set('sector', params.sector);
  if (params.level1) searchParams.set('level1', params.level1);
  if (params.level2) searchParams.set('level2', params.level2);
  if (params.level3) searchParams.set('level3', params.level3);

  const response = await fetch(`/api/scc/hierarchy?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error('Hierarchy request failed');
  }
  return (await response.json()) as string[];
}

export async function fetchSccMatches(params: {
  sector: string;
  level1: string;
  level2: string;
  level3: string;
  level4: string;
}) {
  const searchParams = new URLSearchParams(params);
  const response = await fetch(`/api/scc/search?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error('SCC search request failed');
  }
  return (await response.json()) as SccMatch[];
}

export async function fetchSccCodeMatches(query: string) {
  const searchParams = new URLSearchParams({ query });
  const response = await fetch(`/api/scc/code-search?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error('SCC code search failed');
  }
  return (await response.json()) as SccCodeMatch[];
}

export async function exportBulk(items: CartItem[]) {
  const response = await fetch('/api/export/bulk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items })
  });
  if (!response.ok) {
    throw new Error('Bulk export failed');
  }
  return response;
}

export async function searchAp42Factors(section: string) {
  const searchParams = new URLSearchParams();
  searchParams.append('section', section);
  const response = await fetch(`/api/ap42/search?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error('AP-42 search request failed');
  }
  return (await response.json()) as SearchResponse;
}

export async function exportAp42Selected(factorIds: Array<number | string>) {
  const response = await fetch('/api/ap42/export/selected', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ factor_ids: factorIds })
  });
  if (!response.ok) {
    throw new Error('AP-42 export failed');
  }
  return response;
}

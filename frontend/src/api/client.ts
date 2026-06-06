const BASE_URL = import.meta.env.VITE_API_URL ?? "";

async function get<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(`${BASE_URL}${path}`, window.location.origin);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString());
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`);
  return res.json() as Promise<T>;
}

export interface TrendPoint {
  period_start: string;
  period_type: string;
  county: string;
  region_code: string | null;
  sales_count: number;
  avg_sold_price_sek: number | null;
  avg_price_per_sqm: number | null;
  median_sold_price_sek: number | null;
}

export interface RegionSummary {
  county: string;
  region_code: string | null;
  total_sales: number;
  avg_sold_price_sek: number | null;
  avg_price_per_sqm: number | null;
  median_sold_price_sek: number | null;
  avg_living_area_sqm: number | null;
  price_per_sqm_rank: number;
  sales_volume_rank: number;
}

export const api = {
  trends: (params?: { county?: string; period_type?: string; limit?: string }) =>
    get<TrendPoint[]>("/trends", params as Record<string, string> | undefined),

  regions: () => get<RegionSummary[]>("/regions"),

  region: (code: string) => get<RegionSummary>(`/regions/${encodeURIComponent(code)}`),
};

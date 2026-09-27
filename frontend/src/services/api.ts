/* eslint-disable @typescript-eslint/no-explicit-any */
/**
 * SalesBrain Navigator — Centralized API Client
 *
 * Provides typed methods for every backend endpoint.
 * Falls back to mock data when the backend is unavailable.
 */

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

// eslint-disable-next-line @typescript-eslint/no-explicit-any

interface FetchOptions {
  timeout?: number;
}

class APIError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'APIError';
    this.status = status;
  }
}

async function request<T>(path: string, options?: FetchOptions & RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), options?.timeout || 10000);

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    });

    clearTimeout(timeoutId);

    if (!res.ok) {
      const body = await res.json().catch(() => ({}));
      throw new APIError(body.detail || body.error || `HTTP ${res.status}`, res.status);
    }

    return res.json();
  } catch (err) {
    clearTimeout(timeoutId);
    if (err instanceof APIError) throw err;
    if (err instanceof DOMException && err.name === 'AbortError') {
      throw new APIError('Request timed out', 408);
    }
    throw new APIError('Backend unavailable', 0);
  }
}

// ---- Health ----
export async function getHealth() {
  return request<{
    status: string;
    version: string;
    timestamp: string;
    dataset_ready: boolean;
    model_ready: boolean;
  }>('/health');
}

// ---- Dashboard ----
export interface KPIMetric {
  label: string;
  value: string;
  trend: 'up' | 'down' | 'neutral';
  trend_value: string | null;
  description: string | null;
}

export async function getDashboardKPIs() {
  return request<{ metrics: KPIMetric[] }>('/dashboard/kpis');
}

export interface TrendPoint {
  period: string;
  sales: number;
  profit: number;
}

export async function getDashboardTrends(year?: number) {
  const params = year ? `?year=${year}` : '';
  return request<{ data: TrendPoint[]; granularity: string }>(`/dashboard/trends${params}`);
}

// ---- Sales ----
export interface CategorySales {
  category: string;
  sales: number;
  profit: number;
}

export async function getSalesByCategory(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<CategorySales[]>(`/sales/by-category${qs}`);
}

export async function getSalesByRegion(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/sales/by-region${qs}`);
}

export async function getSalesByMarket(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/sales/by-market${qs}`);
}

export async function getMonthlySales(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/sales/monthly${qs}`);
}

// ---- Products ----
export interface ProductSummary {
  product_id: string;
  name: string;
  category: string;
  sub_category: string;
  total_sales: number;
  total_profit: number;
  profit_margin: number;
  total_quantity: number;
  avg_discount: number;
  total_shipping_cost: number;
  order_count: number;
  risk_status: 'Low' | 'Medium' | 'High';
}

export interface ProductListResponse {
  products: ProductSummary[];
  total: number;
  page: number;
  page_size: number;
}

export async function getProducts(params: {
  page?: number;
  page_size?: number;
  q?: string;
  category?: string;
  region?: string;
  market?: string;
  sort_by?: string;
  sort_order?: string;
}) {
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== '' && v !== 'All') qs.set(k, String(v));
  });
  
  const res = await request<ProductListResponse>(`/products?${qs.toString()}`);
  
  // Explicit API Adapter mapping
  const mappedProducts = res.products.map(p => ({
    id: p.product_id,
    name: p.name,
    category: p.category,
    subCategory: p.sub_category,
    sales: p.total_sales,
    profit: p.total_profit,
    profitMargin: p.profit_margin,
    quantity: p.total_quantity,
    averageDiscount: p.avg_discount,
    shippingCost: p.total_shipping_cost,
    orderCount: p.order_count,
    riskStatus: p.risk_status,
  }));
  
  return { ...res, products: mappedProducts };
}

export async function getProductDetail(productId: string) {
  const p = await request<any>(`/products/${encodeURIComponent(productId)}`);
  return {
    id: p.product_id,
    name: p.name,
    category: p.category,
    subCategory: p.sub_category,
    sales: p.total_sales,
    profit: p.total_profit,
    profitMargin: p.profit_margin,
    quantity: p.total_quantity,
    averageDiscount: p.avg_discount,
    shippingCost: p.total_shipping_cost,
    orderCount: p.order_count,
    riskStatus: p.risk_status,
    markets: p.markets,
    regions: p.regions,
    countries: p.countries,
    monthlyTrend: p.monthly_trend
  };
}

// ---- Customers ----
export interface SegmentAnalytics {
  segment: string;
  sales: number;
  profit: number;
  orders: number;
  customers: number;
  avg_order_value: number;
  margin: number;
}

export async function getCustomerSegments() {
  return request<SegmentAnalytics[]>('/customers/segments');
}

// ---- Geography ----
export async function getGeographySummary() {
  return request<any[]>('/geography/summary');
}

export async function getGeographyCountries(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/geography/countries${qs}`);
}

// ---- Profitability ----
export async function getProfitabilitySummary() {
  return request<any>('/profitability/summary');
}

// ---- Outliers / Risk ----
export interface OutlierSummary {
  lower_fence: number;
  upper_fence: number;
  total_outliers: number;
  outlier_pct: number;
  records: unknown[];
}

export async function getOutliers() {
  return request<OutlierSummary>('/outliers');
}

export async function getRisks(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/risks${qs}`);
}

export async function getOpportunities(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/opportunities${qs}`);
}

// ---- AI / Insights ----
export async function getInsights(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/insights${qs}`);
}

export async function getRecommendations(filters?: Record<string, string>) {
  const qs = filters ? '?' + new URLSearchParams(filters).toString() : '';
  return request<any[]>(`/recommendations${qs}`);
}

export async function getGlobalExplanation() {
  return request<any>('/explanations/global');
}

// ---- Predictions ----
export async function getModelStatus() {
  return request<any>('/models/status');
}

export async function predictProfit(data: {
  category: string;
  sub_category: string;
  segment: string;
  region: string;
  market: string;
  ship_mode: string;
  sales: number;
  quantity: number;
  discount: number;
  shipping_cost: number;
}) {
  return request<any>('/predictions/profit', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ---- Scenarios ----
export async function simulate(data: {
  baseline: {
    category: string;
    sub_category: string;
    segment: string;
    region: string;
    market: string;
    ship_mode: string;
    sales: number;
    quantity: number;
    discount: number;
    shipping_cost: number;
  };
  scenario: {
    discount_delta?: number;
    quantity_change_pct?: number;
    shipping_cost_change_pct?: number;
    sales_change_pct?: number;
  };
}) {
  return request<any>('/simulate', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// ---- Reports ----
export async function getReportTypes() {
  return request<any[]>('/reports/types');
}

export async function exportReport(reportType: string, format: string = 'csv', filters?: Record<string, string>) {
  const res = await fetch(`${API_BASE}/reports/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      report_type: reportType,
      format,
      filters: filters || {},
    }),
  });

  if (!res.ok) throw new APIError('Export failed', res.status);

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${reportType}_report.${format}`;
  a.click();
  URL.revokeObjectURL(url);
}

// ---- Data Explorer ----
export async function getDataSchema() {
  return request<any>('/data/schema');
}

export async function getDataQuality() {
  return request<any>('/data/quality');
}

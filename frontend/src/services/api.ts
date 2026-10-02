/* eslint-disable @typescript-eslint/no-explicit-any */
/**
 * SalesBrain Navigator — Centralized API Client
 *
 * Provides typed methods for every backend endpoint.
 * Falls back to mock data when the backend is unavailable.
 */

let API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';
if (API_BASE && !API_BASE.endsWith('/api/v1')) {
  API_BASE = `${API_BASE}/api/v1`;
}

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

import { auth } from '@/lib/firebase';

async function getAuthToken(): Promise<string | null> {
  const authMode = process.env.NEXT_PUBLIC_AUTH_MODE || 'local';
  if (authMode === 'local') {
    return typeof window !== 'undefined' ? localStorage.getItem('salesbrain_token') : null;
  } else {
    // Firebase mode
    if (!auth) return null;
    await auth.authStateReady();
    if (!auth.currentUser) return null;
    try {
      // Force refresh if needed
      return await auth.currentUser.getIdToken(false);
    } catch (e) {
      console.warn("Failed to get Firebase token:", e);
      return null;
    }
  }
}

async function request<T>(path: string, options?: FetchOptions & RequestInit): Promise<T> {
  const controller = new AbortController();
  const token = await getAuthToken();
  const headers = new Headers(options?.headers);
  if (token) { headers.set('Authorization', `Bearer ${token}`); }
  if (!headers.has('Content-Type')) { headers.set('Content-Type', 'application/json'); }
  const timeoutId = setTimeout(() => controller.abort(), options?.timeout || 10000);

  try {
    const res = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers,
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
    
    if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
      throw new APIError('Network error or CORS policy blocked the request. Please check if the backend is running and reachable.', 0);
    }
    throw new APIError(err instanceof Error ? err.message : 'Backend unavailable', 0);

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
  const token = await getAuthToken();
  if (!token && (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') !== 'local') {
    throw new Error('Authentication required');
  }

  const headers = new Headers({ 'Content-Type': 'application/json' });
  if (token) { headers.set('Authorization', `Bearer ${token}`); }
  if (!headers.has('Content-Type')) { headers.set('Content-Type', 'application/json'); }

  const res = await fetch(`${API_BASE}/reports/export`, {
    method: 'POST',
    headers,
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

// ---- My Data Workspace ----

export async function uploadDataset(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  const token = await getAuthToken();
  if (!token && (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') !== 'local') {
    throw new Error('Authentication required');
  }

  const headers = new Headers();
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 120000); // 2-min timeout for large files

  try {
    const res = await fetch(`${API_BASE}/datasets/upload`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
      headers,
      // Do NOT set Content-Type — browser sets multipart boundary automatically
    });
    clearTimeout(timeoutId);
    if (!res.ok) {
      if (res.status === 401 || res.status === 403) throw new Error("Authentication required or expired. Please sign in again.");
      if (res.status === 413) throw new Error("File is too large. Please upload a smaller dataset.");
      if (res.status >= 500) throw new Error("Server processing failed. The file may be corrupt, unsupported, or the server encountered an error.");
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Upload failed (HTTP ${res.status})`);
    }
    return res.json();
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.message === 'Authentication required') throw err;
    if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
      throw new Error("Network error or CORS policy blocked the upload. The backend may be asleep or unreachable.");
    }
    throw new Error(err.message || 'An unexpected error occurred during upload.');
  }
}

export async function listDatasets(): Promise<any> {
  return request<any>('/datasets');
}

export async function getDatasetMeta(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}`);
}

export async function getDatasetPreview(datasetId: string, rows = 50): Promise<any> {
  return request<any>(`/datasets/${datasetId}/preview?rows=${rows}`);
}

export async function getDatasetSchema(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/schema`);
}

export async function getDatasetQuality(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/quality`);
}

export async function mapDatasetColumns(datasetId: string, mapping: Record<string, string>): Promise<any> {
  return request<any>(`/datasets/${datasetId}/map-columns`, {
    method: 'POST',
    body: JSON.stringify({ mapping }),
  });
}

export async function createWorkspaceDashboard(datasetId: string, mapping?: Record<string, string>): Promise<any> {
  return request<any>(`/datasets/${datasetId}/create-dashboard`, {
    method: 'POST',
    body: JSON.stringify(mapping ? { mapping } : {}),
    timeout: 60000,
  });
}

export async function getWorkspaceDashboard(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/dashboard`);
}

export async function generateWorkspaceInsights(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/generate-insights`, {
    method: 'POST',
    body: '{}',
    timeout: 30000,
  });
}

export async function getWorkspaceInsights(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/insights`);
}

export async function generateWorkspaceRecommendations(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/generate-recommendations`, {
    method: 'POST',
    body: '{}',
    timeout: 30000,
  });
}

export async function getWorkspaceRecommendations(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}/recommendations`);
}

export async function exportWorkspaceReport(datasetId: string, reportType: 'kpis' | 'insights' | 'recommendations' = 'kpis') {
  const token = await getAuthToken();
  if (!token && (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') !== 'local') {
    throw new Error('Authentication required');
  }

  const headers = new Headers();
  if (token) { headers.set('Authorization', `Bearer ${token}`); }
  if (!headers.has('Content-Type')) { headers.set('Content-Type', 'application/json'); }

  const res = await fetch(`${API_BASE}/datasets/${datasetId}/export?report_type=${reportType}`, {
    headers
  });

  if (!res.ok) throw new APIError('Export failed', res.status);

  const blob = await res.blob();
  const downloadUrl = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `workspace_${reportType}.csv`;
  a.click();
  URL.revokeObjectURL(downloadUrl);
}

export async function deleteDataset(datasetId: string): Promise<any> {
  return request<any>(`/datasets/${datasetId}`, { method: 'DELETE' });
}

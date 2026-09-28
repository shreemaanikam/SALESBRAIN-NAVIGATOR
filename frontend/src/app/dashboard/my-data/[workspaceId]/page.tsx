/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import {
  BarChart3, ArrowLeft, Database, TrendingUp, DollarSign,
  Package, Map, Users, Loader2, AlertTriangle, Lightbulb,
  Download, RefreshCw, ExternalLink, ShoppingCart
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell, ScatterChart, Scatter,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import {
  getWorkspaceDashboard,
  createWorkspaceDashboard,
  exportWorkspaceReport,
} from '@/services/api';
import { useWorkspaceStore } from '@/store/store';
import { cn } from '@/lib/utils';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899', '#84cc16'];

function KpiCard({ label, value, icon: Icon }: { label: string; value: string; icon: React.ElementType }) {
  return (
    <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-xl p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">{label}</span>
        <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center">
          <Icon className="w-4 h-4 text-blue-600" />
        </div>
      </div>
      <div className="text-2xl font-bold text-slate-900 dark:text-white truncate" title={value}>{value}</div>
    </div>
  );
}

const KPI_ICONS: Record<string, React.ElementType> = {
  'Total Sales': TrendingUp,
  'Total Profit': DollarSign,
  'Profit Margin': BarChart3,
  'Unique Orders': ShoppingCart,
  'Total Quantity': Package,
  'Avg Discount': Database,
};

export default function WorkspaceDashboardPage() {
  const params = useParams();
  const workspaceId = params.workspaceId as string;
  const { workspaces, activeWorkspace, setActiveWorkspace } = useWorkspaceStore();

  const [dashboard, setDashboard] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [refreshing, setRefreshing] = useState(false);

  // Hydrate active workspace from persisted list
  useEffect(() => {
    if (!activeWorkspace || activeWorkspace.datasetId !== workspaceId) {
      const ws = workspaces.find((w) => w.datasetId === workspaceId);
      if (ws) setActiveWorkspace(ws);
    }
  }, [workspaceId, workspaces, activeWorkspace, setActiveWorkspace]);

  async function loadDashboard() {
    setLoading(true);
    setError('');
    try {
      const res = await getWorkspaceDashboard(workspaceId);
      setDashboard(res.dashboard);
    } catch {
      // Dashboard may not exist yet — try creating it
      try {
        const ws = workspaces.find((w) => w.datasetId === workspaceId);
        if (ws?.mapping && Object.keys(ws.mapping).length > 0) {
          const res = await createWorkspaceDashboard(workspaceId, ws.mapping);
          setDashboard(res.dashboard);
        } else {
          setError('Dashboard not found. Please re-upload and map your dataset.');
        }
      } catch (e2: any) {
        setError(e2.message || 'Could not load dashboard. The workspace may have expired — workspaces are in-memory and cleared on server restart.');
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadDashboard(); }, [workspaceId]); // eslint-disable-line react-hooks/exhaustive-deps

  async function handleRefresh() {
    setRefreshing(true);
    await loadDashboard();
    setRefreshing(false);
  }

  const ws = workspaces.find((w) => w.datasetId === workspaceId) || activeWorkspace;
  const modules = dashboard?.available_modules || {};

  if (loading) return (
    <div className="flex flex-col items-center justify-center h-64 gap-4">
      <Loader2 className="w-10 h-10 animate-spin text-blue-600" />
      <p className="text-slate-500 dark:text-slate-400">Loading your workspace dashboard…</p>
    </div>
  );

  if (error) return (
    <div className="max-w-lg mx-auto mt-12 space-y-4">
      <div className="flex items-start gap-3 p-5 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-xl">
        <AlertTriangle className="w-5 h-5 text-red-500 mt-0.5 shrink-0" />
        <div>
          <p className="font-medium text-red-700 dark:text-red-300">Dashboard Unavailable</p>
          <p className="text-sm text-red-600 dark:text-red-400 mt-1">{error}</p>
        </div>
      </div>
      <div className="flex gap-3">
        <Link href="/dashboard/my-data" className="flex-1 text-center py-2.5 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800">
          <ArrowLeft className="w-4 h-4 inline mr-1" /> My Data
        </Link>
        <Link href="/dashboard/my-data/upload" className="flex-1 text-center py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg">
          Upload New Dataset
        </Link>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <Link href="/dashboard/my-data" className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 mb-2">
            <ArrowLeft className="w-3.5 h-3.5" /> My Data
          </Link>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-blue-600" />
            {ws?.filename ? ws.filename.replace(/\.(csv|xlsx?)$/i, '') : 'Workspace Dashboard'}
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            {ws?.rowCount?.toLocaleString()} rows · Your data · Analytics computed from actual uploaded records
          </p>
        </div>
        <div className="flex gap-2 shrink-0">
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="flex items-center gap-2 px-3 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50"
          >
            <RefreshCw className={cn('w-3.5 h-3.5', refreshing && 'animate-spin')} /> Refresh
          </button>
          <button
            onClick={() => exportWorkspaceReport(workspaceId, 'kpis')}
            className="flex items-center gap-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg"
          >
            <Download className="w-3.5 h-3.5" /> Export KPIs
          </button>
          <Link
            href={`/dashboard/my-data/${workspaceId}/insights`}
            className="flex items-center gap-2 px-3 py-2 border border-blue-200 dark:border-blue-800 text-blue-600 dark:text-blue-400 text-sm font-medium rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20"
          >
            <Lightbulb className="w-3.5 h-3.5" /> Insights <ExternalLink className="w-3 h-3" />
          </Link>
        </div>
      </div>

      {/* Data source banner */}
      <div className="flex items-center gap-2 px-4 py-2 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg text-green-700 dark:text-green-300 text-sm">
        <Database className="w-4 h-4 shrink-0" />
        All analytics below are computed from <strong className="mx-1">{ws?.filename || 'your uploaded file'}</strong> — not from the built-in Superstore dataset.
      </div>

      {/* KPIs */}
      {dashboard?.kpis?.length > 0 && (
        <div className={cn('grid gap-4', dashboard.kpis.length <= 3 ? 'grid-cols-1 sm:grid-cols-3' : 'grid-cols-2 md:grid-cols-3 xl:grid-cols-6')}>
          {dashboard.kpis.map((kpi: any) => (
            <KpiCard key={kpi.label} label={kpi.label} value={kpi.value} icon={KPI_ICONS[kpi.label] || BarChart3} />
          ))}
        </div>
      )}

      {/* Sales Trend */}
      {modules.sales_trend && dashboard.sales_trend?.length > 0 && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-blue-600" /> Sales Trend Over Time
            </CardTitle>
            <CardDescription className="dark:text-slate-400">Monthly sales from your uploaded dataset</CardDescription>
          </CardHeader>
          <CardContent className="p-6">
            <ResponsiveContainer width="100%" height={260}>
              <AreaChart data={dashboard.sales_trend}>
                <defs>
                  <linearGradient id="wsSalesGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="period" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <Tooltip formatter={(v: any) => [`$${Number(v)?.toLocaleString()}`, 'Sales']} />
                <Area type="monotone" dataKey="sales" stroke="#3b82f6" fill="url(#wsSalesGrad)" strokeWidth={2} dot={false} />
                {dashboard.sales_trend[0]?.profit !== undefined && (
                  <Area type="monotone" dataKey="profit" stroke="#10b981" fill="none" strokeWidth={2} strokeDasharray="4 2" dot={false} />
                )}
                <Legend />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {!modules.sales_trend && (
        <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded-lg text-sm text-amber-700 dark:text-amber-300 flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0" /> Sales trend unavailable — no date column was mapped.
        </div>
      )}

      {/* Category + Product */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Category Breakdown */}
        {modules.category_breakdown && dashboard.category_breakdown?.length > 0 && (
          <Card className="dark:bg-slate-900 dark:border-slate-800">
            <CardHeader>
              <CardTitle className="dark:text-white flex items-center gap-2"><Package className="w-4 h-4 text-blue-600" /> Category Sales</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <ResponsiveContainer width="100%" height={240}>
                <BarChart data={dashboard.category_breakdown} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis type="number" tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                  <YAxis type="category" dataKey="name" width={100} tick={{ fontSize: 11, fill: '#94a3b8' }} />
                  <Tooltip formatter={(v: any) => [`$${Number(v)?.toLocaleString()}`, 'Sales']} />
                  <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]}>
                    {dashboard.category_breakdown.map((_: any, i: number) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )}

        {/* Geographic */}
        {modules.geographic && dashboard.geographic?.length > 0 && (
          <Card className="dark:bg-slate-900 dark:border-slate-800">
            <CardHeader>
              <CardTitle className="dark:text-white flex items-center gap-2"><Map className="w-4 h-4 text-blue-600" /> Sales by Region</CardTitle>
            </CardHeader>
            <CardContent className="p-6">
              <ResponsiveContainer width="100%" height={240}>
                <PieChart>
                  <Pie data={dashboard.geographic} dataKey="sales" nameKey="name" cx="50%" cy="50%" outerRadius={90} label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}>
                    {dashboard.geographic.map((_: any, i: number) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(v: any) => [`$${Number(v)?.toLocaleString()}`, 'Sales']} />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Segment */}
      {modules.segment_analysis && dashboard.segment?.length > 0 && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white flex items-center gap-2"><Users className="w-4 h-4 text-blue-600" /> Segment Performance</CardTitle>
          </CardHeader>
          <CardContent className="p-6">
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={dashboard.segment}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#94a3b8' }} />
                <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <Tooltip formatter={(v: any) => [`$${Number(v)?.toLocaleString()}`]} />
                <Bar dataKey="sales" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Sales" />
                {dashboard.segment[0]?.profit !== undefined && (
                  <Bar dataKey="profit" fill="#10b981" radius={[4, 4, 0, 0]} name="Profit" />
                )}
                <Legend />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Profitability Quadrant */}
      {modules.profitability && dashboard.profitability_quadrant?.length > 0 && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white flex items-center gap-2"><DollarSign className="w-4 h-4 text-blue-600" /> Profitability Quadrant</CardTitle>
            <CardDescription className="dark:text-slate-400">Sales vs. Profit by category/product. Points above zero = profitable.</CardDescription>
          </CardHeader>
          <CardContent className="p-6">
            <ResponsiveContainer width="100%" height={300}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="sales" name="Sales" tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <YAxis dataKey="profit" name="Profit" tick={{ fontSize: 11, fill: '#94a3b8' }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} formatter={(v: any) => `$${Number(v)?.toLocaleString()}`} />
                <Scatter data={dashboard.profitability_quadrant} fill="#3b82f6" opacity={0.7} />
              </ScatterChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Product top 10 table */}
      {modules.product_performance && dashboard.product_performance?.length > 0 && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white flex items-center gap-2"><Package className="w-4 h-4 text-blue-600" /> Top Products by Sales</CardTitle>
          </CardHeader>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 dark:bg-slate-800 text-xs text-slate-500 dark:text-slate-400 uppercase">
                <tr>
                  <th className="px-4 py-3 text-left">#</th>
                  <th className="px-4 py-3 text-left">Product</th>
                  <th className="px-4 py-3 text-right">Sales</th>
                  {dashboard.product_performance[0]?.profit !== undefined && <th className="px-4 py-3 text-right">Profit</th>}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {dashboard.product_performance.slice(0, 10).map((p: any, i: number) => (
                  <tr key={i} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <td className="px-4 py-3 text-slate-400">{i + 1}</td>
                    <td className="px-4 py-3 text-slate-900 dark:text-white font-medium truncate max-w-xs">{p.name}</td>
                    <td className="px-4 py-3 text-right font-medium text-slate-900 dark:text-white">${Number(p.sales)?.toLocaleString()}</td>
                    {p.profit !== undefined && (
                      <td className={cn('px-4 py-3 text-right font-medium', p.profit >= 0 ? 'text-green-600' : 'text-red-500')}>
                        ${Number(p.profit)?.toLocaleString()}
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}

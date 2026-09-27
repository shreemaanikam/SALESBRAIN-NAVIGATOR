
/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { mockKpis, mockSalesTrend, mockCategorySales, mockInsights } from '@/data/mock';
import { getDashboardKPIs, getDashboardTrends, getSalesByCategory, getInsights,  } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, 
  BarChart, Bar, Legend
} from 'recharts';
import { ArrowUpRight, ArrowDownRight, AlertCircle, TrendingUp, Lightbulb, Wifi, WifiOff } from 'lucide-react';
import { cn } from '@/lib/utils';

export default function DashboardOverview() {
  // Fetch KPIs from API with mock fallback
  const kpis = useApiData(
    async () => {
      const res = await getDashboardKPIs();
      return res.metrics;
    },
    mockKpis as any as any
  );

  // Fetch trends from API
  const trends = useApiData(
    async () => {
      const res = await getDashboardTrends();
      return res.data;
    },
    mockSalesTrend as any as any
  );

  // Fetch category sales
  const categories = useApiData(
    async () => {
      const res = await getSalesByCategory();
      // Transform to match chart format
      return res.map((c: any) => ({ name: c.category, value: c.sales, profit: c.profit }));
    },
    mockCategorySales as any as any
  );

  // Fetch insights
  const insights = useApiData(
    async () => {
      const res = await getInsights();
      return res.slice(0, 3).map((r: any) => ({
        id: r.id,
        type: r.type === 'risk' ? 'Risk Alert' as const : r.type === 'recommendation' ? 'Recommendation Preview' as const : 'Analytical Insight' as const,
        title: r.title,
        description: r.description || r.insight,
        recommendation: r.recommendation || r.suggested_action,
        impact: r.impact || r.priority,
        affectedEntity: r.affected_entity || r.affectedEntity,
      }));
    },
    mockInsights as any as any
  );

  const isLive = kpis.isFromApi;

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Executive Overview</h1>
          <div className={cn(
            "flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-full",
            isLive ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" : "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400"
          )}>
            {isLive ? <Wifi className="w-3 h-3" /> : <WifiOff className="w-3 h-3" />}
            {isLive ? 'Live Data' : 'Demo Mode'}
          </div>
        </div>
        <p className="text-slate-500 dark:text-slate-400">Business Pulse & Key Performance Indicators.</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {(kpis.data || []).map((kpi: any, index: number) => (
          <Card key={index}>
            <CardContent className="p-6">
              <div className="flex flex-col gap-2">
                <span className="text-sm font-medium text-slate-500 dark:text-slate-400">{kpi.label}</span>
                <span className="text-3xl font-bold text-slate-900 dark:text-white truncate" title={kpi.value}>{kpi.value}</span>
                {kpi.trend_value && (
                  <div className="flex items-center gap-2 mt-1">
                    <span className={cn(
                      "flex items-center text-xs font-medium px-2 py-0.5 rounded-full",
                      kpi.trend === 'up' ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400" : 
                      kpi.trend === 'down' ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" :
                      "bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300"
                    )}>
                      {kpi.trend === 'up' ? <ArrowUpRight className="w-3 h-3 mr-1" /> : <ArrowDownRight className="w-3 h-3 mr-1" />}
                      {kpi.trend_value}
                    </span>
                    {kpi.description && <span className="text-xs text-slate-400 dark:text-slate-500">{kpi.description}</span>}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="dark:text-white">Revenue vs Profit Trend</CardTitle>
            <CardDescription className="dark:text-slate-400">Monthly performance across all regions.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={trends.data || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey={trends.isFromApi ? "period" : "name"} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
                  <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={-10} tickFormatter={(val) => `$${(val/1000)?.toFixed(0)}k`} />
                  <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={10} tickFormatter={(val) => `$${(val/1000)?.toFixed(0)}k`} />
                  <RechartsTooltip 
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Legend verticalAlign="top" height={36} iconType="circle" />
                  <Line yAxisId="left" type="monotone" dataKey="sales" name="Sales" stroke="#2563eb" strokeWidth={3} dot={{ r: 4, fill: '#2563eb' }} activeDot={{ r: 6 }} />
                  <Line yAxisId="right" type="monotone" dataKey="profit" name="Profit" stroke="#10b981" strokeWidth={3} dot={{ r: 4, fill: '#10b981' }} activeDot={{ r: 6 }} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="dark:text-white">Sales by Category</CardTitle>
            <CardDescription className="dark:text-slate-400">Revenue distribution.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categories.data || []} layout="vertical" margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                  <XAxis type="number" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                  <YAxis type="category" dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#334155', fontWeight: 500 }} width={100} />
                  <RechartsTooltip 
                    cursor={{ fill: '#f1f5f9' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                    formatter={(value: any) => [`$${Number(value)?.toLocaleString()}`, 'Sales']}
                  />
                  <Bar dataKey="value" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Insights + Pulse Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <Lightbulb className="w-5 h-5 text-amber-500" />
              <CardTitle className="dark:text-white">AI Insights & Recommendations</CardTitle>
            </div>
            <CardDescription className="dark:text-slate-400">
              {insights.isFromApi ? 'Evidence-based findings from the analytics engine.' : 'Automated findings from the decision support system.'}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {(insights.data || []).map((insight: any) => (
                <div key={insight.id} className="p-4 border border-slate-100 dark:border-slate-700 rounded-lg bg-slate-50/50 dark:bg-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={cn(
                          "text-[10px] uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full",
                          insight.type === 'Risk Alert' ? "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400" : 
                          insight.type === 'Analytical Insight' ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400" : 
                          "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400"
                        )}>
                          {insight.type}
                        </span>
                      </div>
                      <h4 className="text-sm font-semibold text-slate-900 dark:text-white">{insight.title}</h4>
                      <p className="text-sm text-slate-600 dark:text-slate-300 leading-relaxed">{insight.description}</p>
                      {insight.recommendation && (
                        <div className="mt-3 p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-md">
                          <p className="text-sm font-medium text-slate-900 dark:text-white flex items-center gap-2">
                            <TrendingUp className="w-4 h-4 text-blue-600" />
                            Action: {insight.recommendation}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <CardTitle className="dark:text-white">Business Pulse</CardTitle>
            </div>
            <CardDescription className="dark:text-slate-400">Current health of key business vectors.</CardDescription>
          </CardHeader>
          <CardContent>
             <div className="grid grid-cols-2 gap-4">
                <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-100 dark:border-green-800">
                  <div className="text-sm font-medium text-green-800 dark:text-green-300 mb-1">Revenue</div>
                  <div className="text-xl font-bold text-green-900 dark:text-green-200">Strong</div>
                  <p className="text-xs text-green-700 dark:text-green-400 mt-1">Consistently above target</p>
                </div>
                <div className="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800">
                  <div className="text-sm font-medium text-amber-800 dark:text-amber-300 mb-1">Profitability</div>
                  <div className="text-xl font-bold text-amber-900 dark:text-amber-200">Watch</div>
                  <p className="text-xs text-amber-700 dark:text-amber-400 mt-1">Margin compression detected</p>
                </div>
                <div className="p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-100 dark:border-red-800">
                  <div className="text-sm font-medium text-red-800 dark:text-red-300 mb-1">Discount Pressure</div>
                  <div className="text-xl font-bold text-red-900 dark:text-red-200">High</div>
                  <p className="text-xs text-red-700 dark:text-red-400 mt-1">Impacting bottom line</p>
                </div>
                <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800">
                  <div className="text-sm font-medium text-blue-800 dark:text-blue-300 mb-1">Shipping</div>
                  <div className="text-xl font-bold text-blue-900 dark:text-blue-200">Stable</div>
                  <p className="text-xs text-blue-700 dark:text-blue-400 mt-1">Within normal ranges</p>
                </div>
             </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

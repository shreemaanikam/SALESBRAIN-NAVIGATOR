/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { getCustomerSegments } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';

export default function CustomerIntelligencePage() {
  const mockSegmentData = [
    { name: 'Consumer', segment: 'Consumer', sales: 6500000, profit: 750000, margin: 11.5, orders: 13000, customers: 0, avg_order_value: 0 },
    { name: 'Corporate', segment: 'Corporate', sales: 3800000, profit: 450000, margin: 11.8, orders: 7500, customers: 0, avg_order_value: 0 },
    { name: 'Home Office', segment: 'Home Office', sales: 2342905, profit: 269035, margin: 11.5, orders: 4535, customers: 0, avg_order_value: 0 },
  ];

  const { data: segmentData } = useApiData(getCustomerSegments, mockSegmentData);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Customer & Segment Intelligence</h1>
          <p className="text-slate-500 dark:text-slate-400">Analyze performance across Consumer, Corporate, and Home Office segments.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {(segmentData || []).map((segment) => (
          <Card key={segment.segment || (segment as { name?: string }).name} className="dark:bg-slate-900 dark:border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="dark:text-white text-xl">{segment.segment || (segment as { name?: string }).name}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 mt-2">
                <div>
                  <div className="text-sm text-slate-500 dark:text-slate-400">Total Sales</div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-white break-words">${segment.sales.toLocaleString()}</div>
                </div>
                <div className="grid grid-cols-2 gap-4 border-t border-slate-100 dark:border-slate-800 pt-4">
                  <div className="min-w-0">
                    <div className="text-xs text-slate-500 dark:text-slate-400 truncate">Profit</div>
                    <div className="text-sm font-medium text-green-600 truncate" title={`$${segment.profit.toLocaleString()}`}>${segment.profit.toLocaleString()}</div>
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs text-slate-500 dark:text-slate-400 truncate">Margin</div>
                    <div className="text-sm font-medium text-slate-900 dark:text-white truncate">{segment.margin}%</div>
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs text-slate-500 dark:text-slate-400 truncate">Orders</div>
                    <div className="text-sm font-medium text-slate-900 dark:text-white truncate" title={segment.orders.toLocaleString()}>{segment.orders.toLocaleString()}</div>
                  </div>
                  <div className="min-w-0">
                    <div className="text-xs text-slate-500 dark:text-slate-400 truncate">Avg Order</div>
                    <div className="text-sm font-medium text-slate-900 dark:text-white truncate" title={`$${segment.avg_order_value || 0}`}>${segment.avg_order_value || 0}</div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <CardTitle className="dark:text-white">Segment Profitability Comparison</CardTitle>
          <CardDescription className="dark:text-slate-400">Sales and profit breakdown by customer segment.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={segmentData || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" opacity={0.5} />
                <XAxis dataKey={segmentData?.[0]?.segment ? "segment" : "name"} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dy={10} />
                <YAxis yAxisId="left" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={-10} tickFormatter={(val) => `$${val/1000}k`} />
                <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} dx={10} tickFormatter={(val) => `$${val/1000}k`} />
                <Tooltip 
                  cursor={{ fill: 'transparent' }}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', backgroundColor: 'var(--card)' }}
                  formatter={(value: any, name: any) => [`$${value.toLocaleString()}`, name]}
                />
                <Legend verticalAlign="top" height={36} iconType="circle" />
                <Bar yAxisId="left" dataKey="sales" name="Sales" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={40} />
                <Bar yAxisId="right" dataKey="profit" name="Profit" fill="#10b981" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

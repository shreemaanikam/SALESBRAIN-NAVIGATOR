/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Globe } from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { getGeographySummary, getGeographyCountries } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';

export default function GeographyIntelligencePage() {
  const mockMarketData = [
    { name: 'APAC', market: 'APAC', sales: 4000000, profit: 450000 },
    { name: 'EU', market: 'EU', sales: 3500000, profit: 420000 },
    { name: 'US', market: 'US', sales: 3000000, profit: 380000 },
    { name: 'LATAM', market: 'LATAM', sales: 1500000, profit: 120000 },
    { name: 'EMEA', market: 'EMEA', sales: 642905, profit: 99035 },
  ];

  const mockCountryData = [
    { country: 'United States', market: 'US', sales: 3000000, profit: 380000, margin: 12.6 },
    { country: 'Australia', market: 'APAC', sales: 1200000, profit: 150000, margin: 12.5 },
    { country: 'France', market: 'EU', sales: 950000, profit: 110000, margin: 11.5 },
  ];

  const { data: marketData } = useApiData(getGeographySummary, mockMarketData);
  const { data: countryData } = useApiData(() => getGeographyCountries(), mockCountryData);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-3">
            <Globe className="w-8 h-8 text-blue-600" />
            Geography Intelligence
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Market and regional performance distribution.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white">Sales by Market</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={marketData || []} layout="vertical" margin={{ top: 0, right: 0, left: 20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" opacity={0.5} />
                  <XAxis type="number" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} tickFormatter={(val) => `$${val/1000000}M`} />
                  <YAxis type="category" dataKey={marketData?.[0]?.market ? "market" : "name"} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                  <Tooltip 
                    cursor={{ fill: 'transparent' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', backgroundColor: 'var(--card)' }}
                    formatter={(value: any) => [`$${value.toLocaleString()}`, 'Sales']}
                  />
                  <Bar dataKey="sales" fill="#3b82f6" radius={[0, 4, 4, 0]} barSize={24} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white">Profit by Market</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-80 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={marketData || []} layout="vertical" margin={{ top: 0, right: 0, left: 20, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" opacity={0.5} />
                  <XAxis type="number" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} tickFormatter={(val) => `$${val/1000}k`} />
                  <YAxis type="category" dataKey={marketData?.[0]?.market ? "market" : "name"} axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b' }} />
                  <Tooltip 
                    cursor={{ fill: 'transparent' }}
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)', backgroundColor: 'var(--card)' }}
                    formatter={(value: any) => [`$${value.toLocaleString()}`, 'Profit']}
                  />
                  <Bar dataKey="profit" fill="#10b981" radius={[0, 4, 4, 0]} barSize={24} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <CardTitle className="dark:text-white">Country Ranking Top 10</CardTitle>
          <CardDescription className="dark:text-slate-400">The highest performing countries by total sales volume.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-slate-500 dark:text-slate-400 uppercase bg-slate-50 dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700">
                <tr>
                  <th className="px-6 py-4 font-semibold">Rank</th>
                  <th className="px-6 py-4 font-semibold">Country</th>
                  <th className="px-6 py-4 font-semibold">Market</th>
                  <th className="px-6 py-4 font-semibold text-right">Sales</th>
                  <th className="px-6 py-4 font-semibold text-right">Profit</th>
                  <th className="px-6 py-4 font-semibold text-right">Margin</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                {(countryData || []).slice(0, 10).map((row: any, index: number) => (
                  <tr key={index} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                    <td className="px-6 py-4 text-slate-900 dark:text-slate-300">{index + 1}</td>
                    <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{row.country}</td>
                    <td className="px-6 py-4 text-slate-500 dark:text-slate-400">{row.market}</td>
                    <td className="px-6 py-4 text-right font-medium text-slate-900 dark:text-white">${row.sales.toLocaleString()}</td>
                    <td className="px-6 py-4 text-right font-medium text-green-600">${row.profit.toLocaleString()}</td>
                    <td className="px-6 py-4 text-right text-slate-900 dark:text-white">{row.margin}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

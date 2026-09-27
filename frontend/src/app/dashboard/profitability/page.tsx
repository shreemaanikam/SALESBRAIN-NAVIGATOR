/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import {  } from '@/data/mock';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip as RechartsTooltip, Cell } from 'recharts';
import { getProfitabilitySummary } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';

export default function ProfitabilityPage() {
  // Mock data for the profitability quadrant (Sales vs Profit)
  const mockQuadrantData = [
    { id: 1, name: "Printers", sales: 120000, profit: 30000, margin: 25 },
    { id: 2, name: "Copiers", sales: 150000, profit: 45000, margin: 30 },
    { id: 3, name: "Bookcases", sales: 110000, profit: -12000, margin: -10 },
    { id: 4, name: "Tables", sales: 180000, profit: -25000, margin: -14 },
    { id: 5, name: "Phones", sales: 200000, profit: 25000, margin: 12.5 },
    { id: 6, name: "Accessories", sales: 85000, profit: 18000, margin: 21 },
    { id: 7, name: "Chairs", sales: 160000, profit: 5000, margin: 3 },
    { id: 8, name: "Machines", sales: 190000, profit: -5000, margin: -2.6 },
    { id: 9, name: "Paper", sales: 40000, profit: 18000, margin: 45 },
    { id: 10, name: "Binders", sales: 90000, profit: 22000, margin: 24 },
  ];

  const { data: profitabilitySummary } = useApiData(getProfitabilitySummary, { subcategories: mockQuadrantData });
  const quadrantData = profitabilitySummary?.subcategories || mockQuadrantData;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Profitability Intelligence</h1>
          <p className="text-slate-500">Analyze the relationship between revenue, profit, margins, and discounts.</p>
        </div>
      </div>

      <Card className="overflow-hidden">
        <CardHeader>
          <CardTitle>Profitability Quadrant</CardTitle>
          <CardDescription>Sales vs Profit classification across sub-categories. Size represents margin.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-[500px] w-full relative border border-slate-100 rounded-xl bg-slate-50/30">
            {/* Quadrant Backgrounds */}
            <div className="absolute inset-0 grid grid-cols-2 grid-rows-2 pointer-events-none opacity-50 rounded-xl overflow-hidden">
              <div className="border-r border-b border-slate-200 bg-amber-50/50 flex items-center justify-center">
                <span className="text-slate-400 font-medium text-sm">Low Sales / High Profit</span>
              </div>
              <div className="border-b border-slate-200 bg-green-50/50 flex items-center justify-center">
                <span className="text-slate-400 font-medium text-sm">High Sales / High Profit</span>
              </div>
              <div className="border-r border-slate-200 bg-slate-50/50 flex items-center justify-center">
                <span className="text-slate-400 font-medium text-sm">Low Sales / Low Profit</span>
              </div>
              <div className="bg-red-50/50 flex items-center justify-center">
                <span className="text-slate-400 font-medium text-sm">High Sales / Low Profit</span>
              </div>
            </div>

            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" opacity={0.5} />
                <XAxis 
                  type="number" 
                  dataKey="sales" 
                  name="Sales" 
                  tickFormatter={(val) => `$${val/1000}k`}
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: '#64748b' }}
                />
                <YAxis 
                  type="number" 
                  dataKey="profit" 
                  name="Profit"
                  tickFormatter={(val) => `$${val/1000}k`}
                  axisLine={false}
                  tickLine={false}
                  tick={{ fontSize: 12, fill: '#64748b' }}
                />
                <ZAxis type="number" dataKey="margin" range={[100, 1000]} name="Margin" />
                <RechartsTooltip 
                  cursor={{ strokeDasharray: '3 3' }}
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  formatter={(value: any, name: any) => {
                    if (name === 'Margin') return [`${value}%`, name];
                    return [`$${value.toLocaleString()}`, name];
                  }}
                  labelFormatter={() => ''}
                />
                <Scatter name="Sub-Categories" data={quadrantData}>
                  {quadrantData.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={entry.profit >= 0 ? (entry.sales > 120000 ? '#10b981' : '#f59e0b') : (entry.sales > 120000 ? '#ef4444' : '#64748b')} fillOpacity={0.7} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

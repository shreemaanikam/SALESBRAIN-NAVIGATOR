/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { Database } from 'lucide-react';
import { getDataSchema, getDataQuality } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';

export default function DataExplorerPage() {
  const mockSchema = [
    { name: 'Row ID', type: 'integer', description: 'Unique row identifier' },
    { name: 'Order ID', type: 'string', description: 'Unique identifier for the order' },
    { name: 'Order Date', type: 'date', description: 'Date the order was placed' },
    { name: 'Ship Date', type: 'date', description: 'Date the order was shipped' },
    { name: 'Ship Mode', type: 'string', description: 'Shipping method used' },
    { name: 'Customer ID', type: 'string', description: 'Unique customer identifier' },
    { name: 'Customer Name', type: 'string', description: 'Name of the customer' },
    { name: 'Segment', type: 'string', description: 'Consumer, Corporate, Home Office' },
    { name: 'Country', type: 'string', description: 'Country of the sale' },
    { name: 'City', type: 'string', description: 'City of the sale' },
    { name: 'State', type: 'string', description: 'State of the sale' },
    { name: 'Postal Code', type: 'string', description: 'Postal code' },
    { name: 'Region', type: 'string', description: 'Geographic region of the sale' },
    { name: 'Product ID', type: 'string', description: 'Unique identifier for the product' },
    { name: 'Category', type: 'string', description: 'High-level product category' },
    { name: 'Sub-Category', type: 'string', description: 'Detailed product category' },
    { name: 'Product Name', type: 'string', description: 'Name of the product' },
    { name: 'Sales', type: 'numeric', description: 'Revenue generated from the sale' },
    { name: 'Quantity', type: 'integer', description: 'Number of items purchased' },
    { name: 'Discount', type: 'numeric', description: 'Discount applied to the sale' },
    { name: 'Profit', type: 'numeric', description: 'Net profit from the sale' },
    { name: 'Margin', type: 'numeric', description: 'Calculated margin' },
  ];

  const { data: schemaData } = useApiData(getDataSchema, { schema: mockSchema });
  const schema = schemaData?.schema || mockSchema;
  const { data: qualityData } = useApiData(getDataQuality, { total_rows: 51290, columns: 28, missing_values_pct: 0, quality_score: 'High' });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-3">
            <Database className="w-8 h-8 text-blue-600" />
            Data Explorer
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Inspect the underlying semantic model and raw dataset.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Total Rows</div>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">{qualityData?.total_rows?.toLocaleString() ?? 51290}</div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Columns</div>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">{qualityData?.column_count ?? 28}</div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Missing Values</div>
            <div className="text-3xl font-bold text-green-600">{qualityData?.missing_values_pct ?? 0}%</div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 dark:text-slate-400 mb-1">Data Quality</div>
            <div className="text-3xl font-bold text-blue-600">{qualityData?.quality_score ?? 'High'}</div>
          </CardContent>
        </Card>
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <CardTitle className="dark:text-white">Dataset Schema</CardTitle>
          <CardDescription className="dark:text-slate-400">Primary fields available for analysis and ML predictions.</CardDescription>
        </CardHeader>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left border-t border-slate-100 dark:border-slate-800">
            <thead className="text-xs text-slate-500 dark:text-slate-400 uppercase bg-slate-50 dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700">
              <tr>
                <th className="px-6 py-4 font-semibold">Column Name</th>
                <th className="px-6 py-4 font-semibold">Data Type</th>
                <th className="px-6 py-4 font-semibold">Description</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {schema.map((col: { name: string; type: string; non_null: number; missing: number }, idx: number) => (
                <tr key={idx} className="bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800/50">
                  <td className="px-6 py-4 font-medium text-slate-900 dark:text-white font-mono text-xs">{col.name}</td>
                  <td className="px-6 py-4">
                    <span className="bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 px-2 py-1 rounded text-xs font-medium">
                      {col.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{col.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

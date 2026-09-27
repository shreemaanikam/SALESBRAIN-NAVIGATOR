/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { ArrowRight, ShieldAlert } from 'lucide-react';
import { mockOutliers } from '@/data/mock';
import Link from 'next/link';
import { getOutliers } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';

export default function RiskCenterPage() {
  const { data: outlierData } = useApiData(getOutliers, {
    lower_fence: -299,
    upper_fence: 581,
    total_outliers: 5655,
    outlier_pct: 11.03,
    records: mockOutliers
  });

  const displayRecords = outlierData?.records || mockOutliers;
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-3">
            <ShieldAlert className="w-8 h-8 text-red-600" />
            Risk & Outlier Center
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Identify anomalies, loss-leaders, and margin compression risks.</p>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-900 rounded-lg p-6 border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-2">Unusual Sales and Profit Values</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400 mb-6">
          The following metrics are derived directly from the primary dataset using statistical anomaly detection (IQR) on Sales & Profit. 
          Outliers account for approximately 11.03% of the dataset.
        </p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-md border border-slate-100 dark:border-slate-700">
            <div className="text-xs text-slate-500 dark:text-slate-400 uppercase font-semibold">Lower Fence</div>
            <div className="text-xl font-bold text-red-600">{outlierData?.lower_fence.toFixed(0)}</div>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-md border border-slate-100 dark:border-slate-700">
            <div className="text-xs text-slate-500 dark:text-slate-400 uppercase font-semibold">Upper Fence</div>
            <div className="text-xl font-bold text-blue-600">{outlierData?.upper_fence.toFixed(0)}</div>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-md border border-slate-100 dark:border-slate-700">
            <div className="text-xs text-slate-500 dark:text-slate-400 uppercase font-semibold">Total Outliers</div>
            <div className="text-xl font-bold text-slate-900 dark:text-white">{outlierData?.total_outliers.toLocaleString()}</div>
          </div>
          <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-md border border-slate-100 dark:border-slate-700">
            <div className="text-xs text-slate-500 dark:text-slate-400 uppercase font-semibold">Outlier Ratio</div>
            <div className="text-xl font-bold text-amber-600">{outlierData?.outlier_pct.toFixed(2)}%</div>
          </div>
        </div>
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <CardHeader>
          <CardTitle className="dark:text-white">High Priority Anomalies</CardTitle>
          <CardDescription className="dark:text-slate-400">Transactions flagged by the anomaly detection model requiring immediate review.</CardDescription>
        </CardHeader>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left border-t border-slate-100 dark:border-slate-800">
            <thead className="text-xs text-slate-500 dark:text-slate-400 uppercase bg-slate-50 dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700">
              <tr>
                <th className="px-6 py-4 font-semibold">Order ID</th>
                <th className="px-6 py-4 font-semibold">Type</th>
                <th className="px-6 py-4 font-semibold text-right">Sales</th>
                <th className="px-6 py-4 font-semibold text-right">Profit</th>
                <th className="px-6 py-4 font-semibold text-right">Discount</th>
                <th className="px-6 py-4 font-semibold">Severity</th>
                <th className="px-6 py-4 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {displayRecords.slice(0, 50).map((outlier: any, index: number) => (
                <tr key={outlier.id || outlier.order_id || index} className="bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                  <td className="px-6 py-4 font-medium text-slate-900 dark:text-white font-mono text-xs">{outlier.orderId || outlier.order_id}</td>
                  <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{outlier.type || 'Outlier'}</td>
                  <td className="px-6 py-4 text-right font-medium text-slate-900 dark:text-white">${(outlier.sales || 0).toLocaleString()}</td>
                  <td className="px-6 py-4 text-right font-medium text-red-600">${(outlier.profit || 0).toLocaleString()}</td>
                  <td className="px-6 py-4 text-right text-slate-600 dark:text-slate-400">{((outlier.discount || 0) * 100).toFixed(0)}%</td>
                  <td className="px-6 py-4">
                    <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-semibold uppercase">
                      {outlier.severity || 'HIGH'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Link href={`/dashboard/products/${outlier.product_id || 'TEC-PH-10004977'}`} className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium text-sm inline-flex items-center gap-1">
                      Drill-down <ArrowRight className="w-3 h-3" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { ArrowLeft,  AlertTriangle, Lightbulb, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { mockProducts } from '@/data/mock';
import { getProductDetail } from '@/services/api';
// eslint-disable-next-line @typescript-eslint/no-explicit-any
import { useApiData } from '@/hooks/useApiData';

export default function ProductDetailPage({ params }: { params: { id: string } }) {
  const fallbackProduct = mockProducts.find(p => p.id === params.id) || null;
  
  const { data: product, loading } = useApiData(
    () => getProductDetail(params.id),
    fallbackProduct as any,
    [params.id]
  );

  if (loading && !product) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
        <div className="w-16 h-16 bg-slate-100 dark:bg-slate-800 rounded-full flex items-center justify-center mb-4">
          <AlertTriangle className="w-8 h-8 text-slate-400" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Product Not Found</h2>
        <p className="text-slate-500 dark:text-slate-400 max-w-md">
          The product ID &quot;{params.id}&quot; does not exist in the current dataset.
        </p>
        <Link href="/dashboard/products" className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
          Return to Products
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/dashboard/products" className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md transition-colors text-slate-500 dark:text-slate-400">
          <ArrowLeft className="w-5 h-5" />
        </Link>
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 uppercase tracking-wider">{product.category}</span>
            <span className="text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 uppercase tracking-wider">{product.subCategory}</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">{product.name}</h1>
          <p className="text-slate-500 dark:text-slate-400 font-mono text-sm mt-1">{product.id}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 mb-1">Total Revenue</div>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {product.sales != null ? `$${product.sales.toLocaleString()}` : 'N/A'}
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 mb-1">Net Profit</div>
            <div className={cn("text-3xl font-bold", (product.profit ?? 0) < 0 ? "text-red-600" : "text-green-600")}>
              {product.profit != null ? `$${product.profit.toLocaleString()}` : 'N/A'}
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 mb-1">Profit Margin</div>
            <div className={cn("text-3xl font-bold", (product.profitMargin ?? 0) < 0 ? "text-red-600" : "text-slate-900 dark:text-white")}>
              {product.profitMargin != null ? `${product.profitMargin}%` : 'N/A'}
            </div>
          </CardContent>
        </Card>
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardContent className="p-6">
            <div className="text-sm font-medium text-slate-500 mb-1">Average Discount</div>
            <div className="text-3xl font-bold text-slate-900 dark:text-white">
              {product.averageDiscount != null ? `${(product.averageDiscount * 100).toFixed(0)}%` : 'N/A'}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Sales vs Profit Margin Over Time</CardTitle>
              <CardDescription>Historical performance metrics.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[300px] flex items-center justify-center bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-slate-400">Chart Visualization Space</span>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-amber-500" />
                <CardTitle>Demo Insight</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {product.profit < 0 ? (
                <>
                  <p className="text-sm text-slate-700">
                    This product is generating high sales volume but resulting in net losses due to a combination of high discounts ({product.averageDiscount != null ? (product.averageDiscount * 100).toFixed(0) : 'N/A'}%) and shipping costs.
                  </p>
                  <div className="bg-blue-50 border border-blue-100 rounded-md p-3">
                    <span className="text-xs font-bold uppercase text-blue-700 block mb-1">Recommendation Preview</span>
                    <p className="text-sm text-blue-900">Cap maximum discount at 15% and switch to standard shipping for non-corporate accounts.</p>
                  </div>
                </>
              ) : (
                <>
                  <p className="text-sm text-slate-700">
                    This product maintains strong profitability ({product.profitMargin}%) across multiple regions with minimal discount dependency.
                  </p>
                  <div className="bg-blue-50 border border-blue-100 rounded-md p-3">
                    <span className="text-xs font-bold uppercase text-blue-700 block mb-1">Recommendation Preview</span>
                    <p className="text-sm text-blue-900">Consider promotional campaigns in underperforming regions to scale volume.</p>
                  </div>
                </>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Risk Profile</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                  <span className="text-sm text-slate-600">Overall Risk Status</span>
                  <span className={cn(
                    "px-2 py-1 rounded text-xs font-bold uppercase",
                    product.riskStatus === 'High' ? "bg-red-100 text-red-700" : 
                    product.riskStatus === 'Medium' ? "bg-amber-100 text-amber-700" : "bg-green-100 text-green-700"
                  )}>
                    {product.riskStatus}
                  </span>
                </div>
                <div className="flex justify-between items-center pb-3 border-b border-slate-100">
                  <span className="text-sm text-slate-600">Margin Compression Risk</span>
                  <span className="text-sm font-medium text-slate-900">{product.profitMargin < 10 ? 'Elevated' : 'Low'}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-sm text-slate-600">Shipping Cost Impact</span>
                  <span className="text-sm font-medium text-slate-900">${product.shippingCost} / order</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

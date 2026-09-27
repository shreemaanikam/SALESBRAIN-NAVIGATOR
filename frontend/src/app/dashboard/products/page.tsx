/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React, { useState } from 'react';
import { Card,  } from '@/components/ui/Card';
import { mockProducts } from '@/data/mock';
import Link from 'next/link';
import { ArrowUpDown, ChevronLeft, ChevronRight, Loader2 } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useFilterStore } from '@/store/store';
import { getProducts } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';


export default function ProductIntelligencePage() {
  const { searchQuery, category, region } = useFilterStore();
  const [currentPage, setCurrentPage] = useState(1);
  const [sortField, setSortField] = useState<'sales' | 'profit' | 'name'>('sales');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  
  const itemsPerPage = 5;

  const { data, loading } = useApiData(
    () => getProducts({
      page: currentPage,
      page_size: itemsPerPage,
      q: searchQuery,
      category,
      region,
      sort_by: sortField,
      sort_order: sortOrder
    }),
    { products: mockProducts.slice(0, 5), total: mockProducts.length, page: 1, page_size: 5 },
    [currentPage, searchQuery, category, region, sortField, sortOrder]
  );

  const paginatedProducts = data?.products || [];
  const totalItems = data?.total || 0;
  const totalPages = Math.ceil(totalItems / itemsPerPage) || 1;

  const handleSort = (field: 'sales' | 'profit' | 'name') => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
    setCurrentPage(1);
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white">Product Intelligence</h1>
          <p className="text-slate-500 dark:text-slate-400">Deep dive into SKU-level performance and risk.</p>
        </div>
      </div>

      <Card className="dark:bg-slate-900 dark:border-slate-800">
        <div className="p-4 border-b border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-slate-500 dark:text-slate-400">{totalItems} Results {loading && <Loader2 className="w-4 h-4 animate-spin inline ml-2" />}</span>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-slate-500 dark:text-slate-400 uppercase bg-slate-50 dark:bg-slate-800 border-b border-slate-100 dark:border-slate-700">
              <tr>
                <th className="px-6 py-4 font-semibold cursor-pointer hover:text-slate-900 dark:hover:text-white" onClick={() => handleSort('name')}>
                  <div className="flex items-center gap-1">Product <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th className="px-6 py-4 font-semibold">Category</th>
                <th className="px-6 py-4 font-semibold">Region</th>
                <th className="px-6 py-4 font-semibold cursor-pointer hover:text-slate-900 dark:hover:text-white" onClick={() => handleSort('sales')}>
                  <div className="flex items-center gap-1 justify-end">Sales <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th className="px-6 py-4 font-semibold cursor-pointer hover:text-slate-900 dark:hover:text-white" onClick={() => handleSort('profit')}>
                  <div className="flex items-center gap-1 justify-end">Profit <ArrowUpDown className="w-3 h-3" /></div>
                </th>
                <th className="px-6 py-4 font-semibold text-right">Margin</th>
                <th className="px-6 py-4 font-semibold text-center">Risk</th>
                <th className="px-6 py-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {paginatedProducts.length > 0 ? (
                paginatedProducts.map((product: any) => (
                  <tr key={product.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="font-medium text-slate-900 dark:text-white max-w-[200px] sm:max-w-xs truncate" title={product.name}>{product.name}</div>
                      <div className="text-xs text-slate-500 font-mono mt-0.5 truncate max-w-[200px]">{product.id}</div>
                    </td>
                    <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{product.category}</td>
                    <td className="px-6 py-4 text-slate-600 dark:text-slate-400">{product.subCategory}</td>
                    <td className="px-6 py-4 text-right font-medium text-slate-900 dark:text-white">
                      {product.sales != null ? `$${product.sales?.toLocaleString()}` : 'N/A'}
                    </td>
                    <td className={cn(
                      "px-6 py-4 text-right font-medium",
                      (product.profit ?? 0) < 0 ? "text-red-600" : "text-green-600"
                    )}>
                      {product.profit != null ? `$${product.profit?.toLocaleString()}` : 'N/A'}
                    </td>
                    <td className="px-6 py-4 text-right text-slate-600 dark:text-slate-300">
                      {product.profitMargin != null ? `${product.profitMargin}%` : 'N/A'}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex justify-center">
                        <span className={cn(
                          "px-2.5 py-1 rounded-full text-xs font-semibold uppercase tracking-wider",
                          product.riskStatus === 'High' ? "bg-red-100 text-red-700" : 
                          product.riskStatus === 'Medium' ? "bg-amber-100 text-amber-700" : "bg-green-100 text-green-700"
                        )}>
                          {product.riskStatus}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Link 
                        href={`/dashboard/products/${product.id}`}
                        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium text-sm"
                      >
                        Analyze
                      </Link>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={8} className="px-6 py-12 text-center text-slate-500 dark:text-slate-400">
                    No products found matching the current filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        
        <div className="p-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
          <span className="text-sm text-slate-500 dark:text-slate-400">
            Showing {(currentPage - 1) * itemsPerPage + (paginatedProducts.length > 0 ? 1 : 0)} to {Math.min(currentPage * itemsPerPage, totalItems)} of {totalItems} entries
          </span>
          <div className="flex items-center gap-2">
            <button 
              onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="p-2 border border-slate-200 dark:border-slate-700 rounded-md hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50 transition-colors"
            >
              <ChevronLeft className="w-4 h-4 text-slate-600 dark:text-slate-400" />
            </button>
            <button 
              onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="p-2 border border-slate-200 dark:border-slate-700 rounded-md hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50 transition-colors"
            >
              <ChevronRight className="w-4 h-4 text-slate-600 dark:text-slate-400" />
            </button>
          </div>
        </div>
      </Card>
    </div>
  );
}

/* eslint-disable @typescript-eslint/no-explicit-any */
"use client";

import React from 'react';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/Card';
import { mockInsights } from '@/data/mock';
import { CheckCircle2, ChevronRight, Activity, Cpu } from 'lucide-react';
import { cn } from '@/lib/utils';
import { getInsights } from '@/services/api';
import { useApiData } from '@/hooks/useApiData';
import { Insight } from '@/types';

export default function AIInsightsPage() {
  const { data: insights } = useApiData(getInsights, mockInsights);
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-3">
            <Cpu className="w-8 h-8 text-indigo-600" />
            AI Decision Center
          </h1>
          <p className="text-slate-500 dark:text-slate-400">Explainable AI insights and automated business recommendations.</p>
        </div>
      </div>

      <div className="bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-100 dark:border-indigo-800 p-4 rounded-lg flex items-start gap-4 max-w-4xl">
        <Activity className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-bold text-indigo-900 dark:text-indigo-300">Rule-Based Insight Mode</h4>
          <p className="text-sm text-indigo-700 dark:text-indigo-400">
            Currently displaying static heuristics based on the EDA pipeline. Real AI inference will be available once the Python ML pipeline is fully connected.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 max-w-4xl">
        {((insights as Insight[]) || []).map((insight: Insight, idx: number) => (
          <Card key={insight.id || idx} className={cn(
            "border-l-4 dark:bg-slate-900 dark:border-r-slate-800 dark:border-t-slate-800 dark:border-b-slate-800",
            insight.type === 'Risk Alert' ? "border-l-red-500" : 
            insight.type === 'Analytical Insight' ? "border-l-blue-500" : "border-l-purple-500"
          )}>
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row gap-6">
                <div className="flex-1 space-y-4">
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className={cn(
                        "text-xs uppercase tracking-wider font-semibold px-2 py-0.5 rounded-full",
                        insight.type === 'Risk Alert' ? "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400" : 
                        insight.type === 'Analytical Insight' ? "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400" : "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400"
                      )}>
                        {insight.type}
                      </span>
                      <span className="text-xs text-slate-400 flex items-center gap-1">
                        <Activity className="w-3 h-3" /> {insight.impact} Impact
                      </span>
                    </div>
                    <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-2">{insight.title}</h2>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-1">Why it matters:</h4>
                      <p className="text-slate-600 dark:text-slate-400 leading-relaxed">{insight.description}</p>
                    </div>

                    {insight.recommendation && (
                      <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-4 border border-slate-100 dark:border-slate-700">
                        <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-2 flex items-center gap-2">
                          <CheckCircle2 className="w-4 h-4 text-green-600" />
                          Recommended Action
                        </h4>
                        <p className="text-slate-700 dark:text-slate-300 font-medium">{insight.recommendation}</p>
                        
                        <div className="mt-4 pt-4 border-t border-slate-200 dark:border-slate-700 flex items-center gap-4">
                          <button 
                            onClick={() => alert(`Applying recommendation: ${insight.recommendation}`)}
                            className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors shadow-sm"
                          >
                            Apply Recommendation
                          </button>
                          <button 
                            onClick={() => alert(`Dismissed insight: ${insight.title}`)}
                            className="text-sm font-medium text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors"
                          >
                            Dismiss
                          </button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="w-full md:w-64 bg-slate-50 dark:bg-slate-800 rounded-xl p-4 border border-slate-100 dark:border-slate-700 flex flex-col justify-between">
                  <div>
                    <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Affected Entities</h4>
                    <div className="flex items-center gap-2 bg-white dark:bg-slate-900 px-3 py-2 border border-slate-200 dark:border-slate-700 rounded-md">
                      <span className="text-sm font-medium text-slate-900 dark:text-white">{insight.affectedEntity}</span>
                    </div>
                  </div>
                  
                  <Link href="/dashboard/data" className="mt-6 flex items-center justify-between w-full px-3 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 hover:bg-blue-100 dark:hover:bg-blue-900/50 rounded-md transition-colors">
                    View in Explorer
                    <ChevronRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

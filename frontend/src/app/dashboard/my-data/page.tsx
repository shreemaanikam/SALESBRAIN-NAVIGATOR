/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import React from 'react';
import Link from 'next/link';
import { Upload, Database, BarChart3, Lightbulb, ArrowRight, FolderOpen, Trash2, Calendar, Rows } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import { useWorkspaceStore } from '@/store/store';
import { deleteDataset } from '@/services/api';
import { cn } from '@/lib/utils';

const STEPS = [
  { number: 1, title: 'Upload Dataset', description: 'Drag & drop or browse a CSV or XLSX file (up to 50 MB).' },
  { number: 2, title: 'Validate & Map', description: 'Preview your data and confirm column mappings.' },
  { number: 3, title: 'Dashboard & Insights', description: 'Generate live analytics, evidence-backed insights, and recommendations.' },
];

export default function MyDataPage() {
  const { workspaces, removeWorkspace, setActiveWorkspace } = useWorkspaceStore();

  async function handleDelete(datasetId: string, e: React.MouseEvent) {
    e.preventDefault();
    try {
      await deleteDataset(datasetId);
    } catch { /* workspace may have expired */ }
    removeWorkspace(datasetId);
  }

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center space-y-3 py-6">
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs font-semibold rounded-full uppercase tracking-wide mb-2">
          <Database className="w-3.5 h-3.5" /> My Data Workspace
        </div>
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 dark:text-white">
          Create Your Retail Dashboard
        </h1>
        <p className="text-slate-500 dark:text-slate-400 max-w-xl mx-auto">
          Upload your retail data to understand sales performance, discover product opportunities,
          analyze profitability, and generate evidence-based recommendations.
        </p>
        <div className="flex items-center justify-center gap-4 pt-4">
          <Link
            href="/dashboard/my-data/upload"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition-colors shadow-sm"
          >
            <Upload className="w-4 h-4" /> Upload Dataset
          </Link>
          <a
            href="/sample_retail_data.csv"
            download
            className="inline-flex items-center gap-2 px-6 py-3 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-medium rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
          >
            <FolderOpen className="w-4 h-4" /> View Sample Dataset
          </a>
        </div>
        <p className="text-xs text-slate-400 dark:text-slate-500 mt-2">
          🔒 Your data is analyzed locally and never shared. Workspaces are cleared on server restart (demo mode).
        </p>
      </div>

      {/* How it works */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {STEPS.map((step) => (
          <Card key={step.number} className="border border-slate-100 dark:border-slate-800">
            <CardContent className="p-6">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-full bg-blue-600 text-white text-sm font-bold flex items-center justify-center shrink-0">
                  {step.number}
                </div>
                <h3 className="font-semibold text-slate-900 dark:text-white">{step.title}</h3>
              </div>
              <p className="text-sm text-slate-500 dark:text-slate-400">{step.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Existing workspaces */}
      {workspaces.length > 0 && (
        <div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-white mb-4 flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" /> Your Workspaces
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {workspaces.map((ws) => (
              <Card
                key={ws.datasetId}
                className="border border-slate-100 dark:border-slate-800 hover:border-blue-200 dark:hover:border-blue-700 transition-colors group"
              >
                <CardContent className="p-5">
                  <div className="flex items-start justify-between gap-2 mb-3">
                    <div className="min-w-0">
                      <div className="font-semibold text-slate-900 dark:text-white truncate">{ws.filename}</div>
                      <div className={cn(
                        'text-xs font-medium mt-0.5 capitalize',
                        ws.status === 'dashboard_ready' ? 'text-green-600' : 'text-amber-600'
                      )}>
                        {ws.status.replace(/_/g, ' ')}
                      </div>
                    </div>
                    <button
                      onClick={(e) => handleDelete(ws.datasetId, e)}
                      className="opacity-0 group-hover:opacity-100 p-1.5 rounded text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-all"
                      title="Delete workspace"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                  <div className="flex items-center gap-4 text-xs text-slate-500 dark:text-slate-400 mb-4">
                    <span className="flex items-center gap-1"><Rows className="w-3 h-3" /> {ws.rowCount?.toLocaleString()} rows</span>
                    <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {new Date(ws.createdAt).toLocaleDateString()}</span>
                  </div>
                  <div className="flex gap-2">
                    <Link
                      href={`/dashboard/my-data/${ws.datasetId}`}
                      onClick={() => setActiveWorkspace(ws)}
                      className="flex-1 text-center py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md transition-colors flex items-center justify-center gap-1"
                    >
                      <BarChart3 className="w-3.5 h-3.5" /> Dashboard
                    </Link>
                    <Link
                      href={`/dashboard/my-data/${ws.datasetId}/insights`}
                      onClick={() => setActiveWorkspace(ws)}
                      className="flex-1 text-center py-2 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm font-medium rounded-md hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors flex items-center justify-center gap-1"
                    >
                      <Lightbulb className="w-3.5 h-3.5" /> Insights
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
            <Link
              href="/dashboard/my-data/upload"
              className="flex flex-col items-center justify-center p-6 border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl text-slate-400 hover:border-blue-400 hover:text-blue-500 transition-colors"
            >
              <Upload className="w-6 h-6 mb-2" />
              <span className="text-sm font-medium">Add New Dataset</span>
            </Link>
          </div>
        </div>
      )}

      {/* Feature highlights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[
          { icon: BarChart3, title: 'Dynamic Analytics', text: 'Charts and KPIs are generated from your actual data — not static placeholders.' },
          { icon: Lightbulb, title: 'Evidence-Backed Insights', text: 'Each insight shows the supporting calculation, affected entity, and time period.' },
          { icon: ArrowRight, title: 'Actionable Recommendations', text: 'Rule-based analysis identifies pricing, discount, and margin opportunities.' },
          { icon: Database, title: 'Your Data Stays Isolated', text: 'Workspace analytics never mix with the built-in Superstore dashboard.' },
        ].map((f) => (
          <Card key={f.title} className="border border-slate-100 dark:border-slate-800">
            <CardContent className="p-5 flex gap-4">
              <div className="w-9 h-9 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center shrink-0">
                <f.icon className="w-4.5 h-4.5 text-blue-600" />
              </div>
              <div>
                <div className="font-semibold text-slate-900 dark:text-white text-sm">{f.title}</div>
                <div className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">{f.text}</div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

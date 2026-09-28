/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import {
  Lightbulb, ArrowLeft, BarChart3, Loader2, AlertTriangle,
  Download, RefreshCw, CheckCircle, Info, TrendingUp, ShieldAlert
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/Card';
import {
  generateWorkspaceInsights,
  getWorkspaceInsights,
  generateWorkspaceRecommendations,
  getWorkspaceRecommendations,
  exportWorkspaceReport,
} from '@/services/api';
import { useWorkspaceStore } from '@/store/store';
import { cn } from '@/lib/utils';

const INSIGHT_TYPE_STYLES: Record<string, string> = {
  'Risk Alert': 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-700 text-red-700 dark:text-red-300',
  'Analytical Insight': 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700 text-blue-700 dark:text-blue-300',
  'Opportunity': 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-700 text-green-700 dark:text-green-300',
};

const INSIGHT_ICONS: Record<string, React.ElementType> = {
  'Risk Alert': ShieldAlert,
  'Analytical Insight': TrendingUp,
  'Opportunity': CheckCircle,
};

const PRIORITY_COLORS: Record<string, string> = {
  High: 'text-red-600 bg-red-50 dark:bg-red-900/20',
  Medium: 'text-amber-600 bg-amber-50 dark:bg-amber-900/20',
  Low: 'text-green-600 bg-green-50 dark:bg-green-900/20',
};

function InsightCard({ insight }: { insight: any }) {
  const [expanded, setExpanded] = useState(false);
  const typeStyle = INSIGHT_TYPE_STYLES[insight.type] || INSIGHT_TYPE_STYLES['Analytical Insight'];
  const Icon = INSIGHT_ICONS[insight.type] || Info;

  return (
    <div className={cn('border rounded-xl p-5 space-y-3', typeStyle)}>
      <div className="flex items-start gap-3">
        <Icon className="w-5 h-5 mt-0.5 shrink-0" />
        <div className="flex-1 min-w-0">
          <div className="font-semibold text-slate-900 dark:text-white">{insight.title}</div>
          <div className="text-sm mt-1 opacity-90">{insight.description}</div>
        </div>
        <span className="px-2 py-0.5 text-xs font-medium rounded bg-white/50 dark:bg-black/20 shrink-0">{insight.type}</span>
      </div>

      {insight.affected_entity && (
        <div className="text-xs flex items-center gap-1 opacity-75">
          <span className="font-medium">Affected:</span> {insight.affected_entity}
        </div>
      )}

      {insight.evidence && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs underline underline-offset-2 opacity-70 hover:opacity-100"
        >
          {expanded ? 'Hide' : 'View'} supporting evidence
        </button>
      )}

      {expanded && insight.evidence && (
        <div className="bg-white/40 dark:bg-black/20 rounded-lg p-3 text-xs font-mono space-y-0.5">
          {Object.entries(insight.evidence).map(([k, v]) => (
            <div key={k}>
              <span className="text-slate-500 dark:text-slate-400">{k}:</span>{' '}
              <span className="font-semibold">{typeof v === 'number' ? Number(v)?.toLocaleString() : String(v)}</span>
            </div>
          ))}
          {insight.method && (
            <div className="mt-1 pt-1 border-t border-white/30">
              <span className="text-slate-500 dark:text-slate-400">Method:</span> {insight.method}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function RecommendationCard({ rec }: { rec: any }) {
  const priorityStyle = PRIORITY_COLORS[rec.priority] || PRIORITY_COLORS.Low;

  return (
    <Card className="dark:bg-slate-900 dark:border-slate-800">
      <CardContent className="p-5 space-y-3">
        <div className="flex items-start justify-between gap-3">
          <div className="font-semibold text-slate-900 dark:text-white flex-1">{rec.title}</div>
          <span className={cn('px-2 py-0.5 text-xs font-bold rounded shrink-0', priorityStyle)}>
            {rec.priority}
          </span>
        </div>
        <p className="text-sm text-slate-600 dark:text-slate-400">{rec.insight}</p>
        {rec.affected_entity && (
          <div className="text-xs text-slate-400"><span className="font-medium text-slate-500">Affected:</span> {rec.affected_entity}</div>
        )}
        {rec.metric_values && Object.keys(rec.metric_values).length > 0 && (
          <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3 text-xs space-y-0.5">
            {Object.entries(rec.metric_values).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="text-slate-400">{k.replace(/_/g, ' ')}:</span>
                <span className="font-semibold text-slate-900 dark:text-white">
                  {typeof v === 'number' ? Number(v)?.toLocaleString(undefined, { maximumFractionDigits: 2 }) : String(v)}
                </span>
              </div>
            ))}
          </div>
        )}
        {rec.suggested_action && (
          <div className="flex items-start gap-2 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg text-sm text-blue-700 dark:text-blue-300">
            <CheckCircle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
            <span>{rec.suggested_action}</span>
          </div>
        )}
        {rec.limitations && (
          <p className="text-xs text-slate-400 italic">{rec.limitations}</p>
        )}
      </CardContent>
    </Card>
  );
}

export default function WorkspaceInsightsPage() {
  const params = useParams();
  const workspaceId = params.workspaceId as string;
  const { workspaces, activeWorkspace, setActiveWorkspace } = useWorkspaceStore();

  const [insights, setInsights] = useState<any[]>([]);
  const [recommendations, setRecommendations] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState<'insights' | 'recommendations'>('insights');

  const ws = workspaces.find((w) => w.datasetId === workspaceId) || activeWorkspace;

  useEffect(() => {
    if (!activeWorkspace || activeWorkspace.datasetId !== workspaceId) {
      const found = workspaces.find((w) => w.datasetId === workspaceId);
      if (found) setActiveWorkspace(found);
    }
  }, [workspaceId, workspaces, activeWorkspace, setActiveWorkspace]);

  async function loadAll() {
    setLoading(true);
    setError('');
    try {
      const [ins, recs] = await Promise.allSettled([
        getWorkspaceInsights(workspaceId),
        getWorkspaceRecommendations(workspaceId),
      ]);
      if (ins.status === 'fulfilled') setInsights(ins.value.insights || []);
      if (recs.status === 'fulfilled') setRecommendations(recs.value.recommendations || []);
    } catch { /* non-fatal — will show generate button */ }
    setLoading(false);
  }

  useEffect(() => { loadAll(); }, [workspaceId]); // eslint-disable-line react-hooks/exhaustive-deps

  async function handleGenerate() {
    setGenerating(true);
    setError('');
    try {
      const [insRes, recRes] = await Promise.allSettled([
        generateWorkspaceInsights(workspaceId),
        generateWorkspaceRecommendations(workspaceId),
      ]);
      if (insRes.status === 'fulfilled') setInsights(insRes.value.insights || []);
      if (recRes.status === 'fulfilled') setRecommendations(recRes.value.recommendations || []);
      if (insRes.status === 'rejected' && recRes.status === 'rejected') {
        setError('Could not generate insights. The workspace may have expired.');
      }
    } finally {
      setGenerating(false);
    }
  }

  if (loading) return (
    <div className="flex items-center justify-center h-64 gap-3">
      <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      <p className="text-slate-500">Loading workspace insights…</p>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link href="/dashboard/my-data" className="text-sm text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 flex items-center gap-1">
              <ArrowLeft className="w-3.5 h-3.5" /> My Data
            </Link>
            <span className="text-slate-300 dark:text-slate-600">/</span>
            <Link href={`/dashboard/my-data/${workspaceId}`} className="text-sm text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 flex items-center gap-1">
              <BarChart3 className="w-3.5 h-3.5" /> Dashboard
            </Link>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white flex items-center gap-2">
            <Lightbulb className="w-6 h-6 text-yellow-500" /> Insights & Recommendations
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            {ws?.filename || 'Your dataset'} · Evidence-backed analysis from your actual data
          </p>
        </div>
        <div className="flex gap-2 shrink-0">
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg disabled:opacity-50"
          >
            {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            Regenerate
          </button>
          <button
            onClick={() => exportWorkspaceReport(workspaceId, activeTab === 'insights' ? 'insights' : 'recommendations')}
            className="flex items-center gap-2 px-4 py-2 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-sm rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800"
          >
            <Download className="w-4 h-4" /> Export CSV
          </button>
        </div>
      </div>

      {/* Data source banner */}
      <div className="flex items-center gap-2 px-4 py-2 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg text-green-700 dark:text-green-300 text-sm">
        <CheckCircle className="w-4 h-4 shrink-0" />
        All insights and recommendations below are derived from <strong className="mx-1">{ws?.filename || 'your uploaded file'}</strong>.
      </div>

      {error && (
        <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300 text-sm">
          <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" /> {error}
        </div>
      )}

      {/* Empty state */}
      {insights.length === 0 && recommendations.length === 0 && !error && (
        <div className="text-center py-16 space-y-4">
          <Lightbulb className="w-12 h-12 text-slate-200 dark:text-slate-700 mx-auto" />
          <h2 className="text-lg font-semibold text-slate-700 dark:text-slate-300">No insights yet</h2>
          <p className="text-slate-400 text-sm max-w-sm mx-auto">
            Click <strong>Regenerate</strong> to analyze your dataset and generate insights and recommendations.
          </p>
          <button onClick={handleGenerate} disabled={generating} className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg disabled:opacity-50 inline-flex items-center gap-2">
            {generating ? <Loader2 className="w-4 h-4 animate-spin" /> : <Lightbulb className="w-4 h-4" />}
            Generate Insights & Recommendations
          </button>
        </div>
      )}

      {/* Tabs */}
      {(insights.length > 0 || recommendations.length > 0) && (
        <>
          <div className="flex gap-1 border border-slate-200 dark:border-slate-700 rounded-lg p-1 bg-slate-50 dark:bg-slate-800/50 w-fit">
            {(['insights', 'recommendations'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={cn(
                  'px-4 py-2 text-sm font-medium rounded-md transition-colors capitalize',
                  activeTab === tab
                    ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-white shadow-sm'
                    : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200'
                )}
              >
                {tab} {tab === 'insights' ? `(${insights.length})` : `(${recommendations.length})`}
              </button>
            ))}
          </div>

          {activeTab === 'insights' && (
            <div className="space-y-4">
              {insights.length === 0 ? (
                <p className="text-slate-400 text-sm">No insights generated yet.</p>
              ) : (
                insights.map((ins) => <InsightCard key={ins.id} insight={ins} />)
              )}
            </div>
          )}

          {activeTab === 'recommendations' && (
            <div className="space-y-4">
              {recommendations.length === 0 ? (
                <p className="text-slate-400 text-sm">No recommendations generated yet.</p>
              ) : (
                recommendations.map((rec) => <RecommendationCard key={rec.id} rec={rec} />)
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

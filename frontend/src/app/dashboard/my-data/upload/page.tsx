/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import React, { useState, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  Upload, X, CheckCircle, AlertTriangle, Info, ChevronRight,
  ChevronLeft, Database, BarChart3, Loader2, File as FileIcon, ArrowLeft
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';
import { cn } from '@/lib/utils';
import {
  uploadDataset,
  mapDatasetColumns,
  createWorkspaceDashboard,
  generateWorkspaceInsights,
  generateWorkspaceRecommendations,
} from '@/services/api';
import { useWorkspaceStore } from '@/store/store';

// ── Business concepts that can be mapped ─────────────────────────────────
const CONCEPTS = [
  { key: 'order_id',      label: 'Order ID',       required: false, group: 'order' },
  { key: 'order_date',    label: 'Order Date',      required: false, group: 'order' },
  { key: 'ship_date',     label: 'Ship Date',       required: false, group: 'order' },
  { key: 'sales',         label: 'Sales / Revenue', required: true,  group: 'finance' },
  { key: 'profit',        label: 'Profit',          required: false, group: 'finance' },
  { key: 'quantity',      label: 'Quantity',        required: false, group: 'finance' },
  { key: 'discount',      label: 'Discount',        required: false, group: 'finance' },
  { key: 'shipping_cost', label: 'Shipping Cost',   required: false, group: 'finance' },
  { key: 'product_name',  label: 'Product Name',    required: false, group: 'product' },
  { key: 'product_id',    label: 'Product ID / SKU',required: false, group: 'product' },
  { key: 'category',      label: 'Category',        required: false, group: 'product' },
  { key: 'sub_category',  label: 'Sub-Category',    required: false, group: 'product' },
  { key: 'segment',       label: 'Customer Segment',required: false, group: 'customer' },
  { key: 'customer_name', label: 'Customer Name',   required: false, group: 'customer' },
  { key: 'region',        label: 'Region',          required: false, group: 'geo' },
  { key: 'country',       label: 'Country',         required: false, group: 'geo' },
  { key: 'market',        label: 'Market',          required: false, group: 'geo' },
  { key: 'ship_mode',     label: 'Ship Mode',       required: false, group: 'order' },
  { key: 'order_priority',label: 'Order Priority',  required: false, group: 'order' },
] as const;

const CONCEPT_GROUPS: Record<string, string> = {
  order: 'Order Information',
  finance: 'Financial Metrics',
  product: 'Product Details',
  customer: 'Customer Information',
  geo: 'Geographic Data',
};

type Step = 'upload' | 'preview' | 'map' | 'create';

const STEP_LABELS: Record<Step, string> = {
  upload: 'Upload',
  preview: 'Preview',
  map: 'Map Columns',
  create: 'Create Dashboard',
};

const STEP_ORDER: Step[] = ['upload', 'preview', 'map', 'create'];

export default function UploadWizardPage() {
  const router = useRouter();
  const { addWorkspace } = useWorkspaceStore();

  const [step, setStep] = useState<Step>('upload');
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [mapping, setMapping] = useState<Record<string, string>>({});
  // We no longer need to track validationResult locally as the step check is sufficient.
  const [creating, setCreating] = useState(false);
  const [createProgress, setCreateProgress] = useState('');
  const [error, setError] = useState('');

  const fileInputRef = useRef<HTMLInputElement>(null);

  // ── File selection ─────────────────────────────────────────────────────
  const handleFile = useCallback((f: File) => {
    const ext = f.name.toLowerCase().split('.').pop() || '';
    if (!['csv', 'xlsx', 'xls'].includes(ext)) {
      setError('Please upload a CSV or XLSX file.');
      return;
    }
    if (f.size > 50 * 1024 * 1024) {
      setError('File is larger than 50 MB. Please reduce the file size.');
      return;
    }
    setError('');
    setFile(f);
  }, []);

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  }, [handleFile]);

  // ── Step 1: Upload ─────────────────────────────────────────────────────
  async function handleUpload() {
    if (!file) return;
    setUploading(true);
    setError('');
    try {
      const result = await uploadDataset(file);
      setUploadResult(result);
      // Pre-populate mapping from suggestions
      if (result?.profile?.suggested_mapping) {
        setMapping(result.profile.suggested_mapping);
      }
      setStep('preview');
    } catch (e: any) {
      setError(e.message || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  }

  // ── Step 3: Validate and proceed ──────────────────────────────────────
  async function handleValidateMapping() {
    setError('');
    const filledEntries = Object.entries(mapping).filter(([, v]) => v && v !== '');
    if (filledEntries.length === 0) {
      setError('Please map at least one column before continuing.');
      return;
    }
    // Client-side check: must have at least 'sales'
    const salesMapped = Object.entries(mapping).some(([k, v]) => k === 'sales' && v);
    if (!salesMapped) {
      setError("Please map the 'Sales / Revenue' column — it's required for analytics.");
      return;
    }
    // We proceed to create
    setStep('create');
  }

  // ── Step 4: Create dashboard ──────────────────────────────────────────
  async function handleCreateDashboard() {
    if (!uploadResult?.dataset_id) return;
    setCreating(true);
    setError('');
    const id = uploadResult.dataset_id;

    try {
      setCreateProgress('Confirming column mapping…');
      await mapDatasetColumns(id, mapping);

      setCreateProgress('Computing analytics from your data…');
      await createWorkspaceDashboard(id, mapping);

      setCreateProgress('Generating insights…');
      try { await generateWorkspaceInsights(id); } catch { /* non-fatal */ }

      setCreateProgress('Generating recommendations…');
      try { await generateWorkspaceRecommendations(id); } catch { /* non-fatal */ }

      setCreateProgress('Dashboard ready!');

      addWorkspace({
        datasetId: id,
        filename: uploadResult.filename,
        rowCount: uploadResult.row_count,
        columnCount: uploadResult.column_count,
        mapping,
        status: 'dashboard_ready',
        createdAt: new Date().toISOString(),
      });

      router.push(`/dashboard/my-data/${id}`);
    } catch (e: any) {
      setError(e.message || 'Failed to create dashboard. Please try again.');
    } finally {
      setCreating(false);
      setCreateProgress('');
    }
  }

  const stepIdx = STEP_ORDER.indexOf(step);

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Back */}
      <Link href="/dashboard/my-data" className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-900 dark:hover:text-white transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to My Data
      </Link>

      {/* Progress steps */}
      <div className="flex items-center gap-0">
        {STEP_ORDER.map((s, i) => (
          <React.Fragment key={s}>
            <div className="flex items-center gap-2">
              <div className={cn(
                'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0',
                i < stepIdx ? 'bg-green-500 text-white' :
                i === stepIdx ? 'bg-blue-600 text-white' :
                'bg-slate-100 dark:bg-slate-800 text-slate-400'
              )}>
                {i < stepIdx ? <CheckCircle className="w-4 h-4" /> : i + 1}
              </div>
              <span className={cn(
                'text-sm font-medium hidden sm:block',
                i === stepIdx ? 'text-slate-900 dark:text-white' : 'text-slate-400'
              )}>
                {STEP_LABELS[s]}
              </span>
            </div>
            {i < STEP_ORDER.length - 1 && (
              <div className={cn('flex-1 h-0.5 mx-3', i < stepIdx ? 'bg-green-400' : 'bg-slate-200 dark:bg-slate-700')} />
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Error banner */}
      {error && (
        <div className="flex items-start gap-3 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 rounded-lg text-red-700 dark:text-red-300">
          <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* ── Step 1: Upload ──────────────────────────────────────────────────── */}
      {step === 'upload' && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white">Upload Your Dataset</CardTitle>
            <CardDescription className="dark:text-slate-400">
              Accepted formats: CSV, XLSX. Maximum file size: 50 MB.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 p-6">
            {/* Drop zone */}
            <div
              className={cn(
                'border-2 border-dashed rounded-xl p-10 text-center transition-colors cursor-pointer',
                isDragging ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-slate-200 dark:border-slate-700 hover:border-blue-400'
              )}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={onDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="w-10 h-10 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
              {file ? (
                <div className="space-y-1">
                  <div className="flex items-center justify-center gap-2 text-slate-900 dark:text-white font-medium">
                    <FileIcon className="w-4 h-4 text-blue-600" />
                    {file.name}
                  </div>
                  <p className="text-sm text-slate-400">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              ) : (
                <>
                  <p className="text-slate-600 dark:text-slate-400 font-medium">Drag & drop your file here</p>
                  <p className="text-sm text-slate-400 mt-1">or click to browse</p>
                </>
              )}
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xlsx,.xls"
              className="hidden"
              onChange={(e) => { if (e.target.files?.[0]) handleFile(e.target.files[0]); }}
            />

            {file && (
              <div className="flex items-center gap-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-lg">
                <FileIcon className="w-4 h-4 text-blue-600 shrink-0" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm font-medium text-slate-900 dark:text-white truncate">{file.name}</div>
                  <div className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB</div>
                </div>
                <button onClick={(e) => { e.stopPropagation(); setFile(null); setError(''); }} className="text-slate-400 hover:text-slate-600">
                  <X className="w-4 h-4" />
                </button>
              </div>
            )}

            <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg flex items-start gap-2 text-xs text-slate-500 dark:text-slate-400">
              <Info className="w-3.5 h-3.5 mt-0.5 shrink-0" />
              <span>Your uploaded file is processed on this server only. No data is sent to external services. Workspaces are cleared on server restart.</span>
            </div>

            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className={cn(
                'w-full py-3 rounded-lg font-semibold text-white transition-colors flex items-center justify-center gap-2',
                !file || uploading ? 'bg-slate-300 dark:bg-slate-700 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
              )}
            >
              {uploading ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Uploading and profiling…</>
              ) : (
                <><Upload className="w-4 h-4" /> Upload & Preview</>
              )}
            </button>
          </CardContent>
        </Card>
      )}

      {/* ── Step 2: Preview ──────────────────────────────────────────────────── */}
      {step === 'preview' && uploadResult && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white">Data Preview</CardTitle>
            <CardDescription className="dark:text-slate-400">
              Showing first 50 rows. Verify data looks correct before mapping.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 p-6">
            {/* Summary */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {[
                { label: 'Total Rows', value: uploadResult.row_count?.toLocaleString() },
                { label: 'Columns', value: uploadResult.column_count },
                { label: 'File', value: uploadResult.filename },
                { label: 'Quality', value: uploadResult.quality?.quality_score || 'Good' },
              ].map(({ label, value }) => (
                <div key={label} className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3">
                  <div className="text-xs text-slate-500 dark:text-slate-400 uppercase font-semibold">{label}</div>
                  <div className="text-sm font-bold text-slate-900 dark:text-white truncate">{value}</div>
                </div>
              ))}
            </div>

            {/* Quality warnings */}
            {uploadResult.quality?.warnings?.length > 0 && (
              <div className="p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-700 rounded-lg space-y-1">
                {uploadResult.quality.warnings.map((w: string, i: number) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-amber-700 dark:text-amber-300">
                    <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" /> {w}
                  </div>
                ))}
              </div>
            )}

            {/* Column types */}
            <div>
              <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">Detected Columns</h3>
              <div className="flex flex-wrap gap-2">
                {uploadResult.profile?.numeric_columns?.map((c: string) => (
                  <span key={c} className="px-2 py-0.5 bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 text-xs rounded border border-green-200 dark:border-green-700">{c} <em className="not-italic text-green-400">numeric</em></span>
                ))}
                {uploadResult.profile?.date_columns?.map((c: string) => (
                  <span key={c} className="px-2 py-0.5 bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 text-xs rounded border border-purple-200 dark:border-purple-700">{c} <em className="not-italic text-purple-400">date</em></span>
                ))}
                {uploadResult.profile?.categorical_columns?.slice(0, 12).map((c: string) => (
                  <span key={c} className="px-2 py-0.5 bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs rounded">{c}</span>
                ))}
              </div>
            </div>

            <div className="flex gap-3">
              <button onClick={() => setStep('upload')} className="flex items-center gap-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800">
                <ChevronLeft className="w-4 h-4" /> Back
              </button>
              <button onClick={() => setStep('map')} className="flex-1 flex items-center justify-center gap-2 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
                Map Columns <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ── Step 3: Map Columns ──────────────────────────────────────────────── */}
      {step === 'map' && uploadResult && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white">Map Your Columns</CardTitle>
            <CardDescription className="dark:text-slate-400">
              We&apos;ve auto-suggested mappings. Review and adjust as needed. Only <em>Sales / Revenue</em> is required.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 p-6">
            {Object.entries(CONCEPT_GROUPS).map(([group, groupLabel]) => {
              const groupConcepts = CONCEPTS.filter((c) => c.group === group);
              return (
                <div key={group}>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">{groupLabel}</h3>
                  <div className="space-y-2">
                    {groupConcepts.map((concept) => (
                      <div key={concept.key} className="flex items-center gap-3">
                        <label className="w-40 shrink-0 text-sm text-slate-700 dark:text-slate-300">
                          {concept.label}
                          {concept.required && <span className="text-red-500 ml-0.5">*</span>}
                        </label>
                        <select
                          value={mapping[concept.key] || ''}
                          onChange={(e) => setMapping((m) => ({ ...m, [concept.key]: e.target.value }))}
                          className="flex-1 text-sm border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                          <option value="">— not mapped —</option>
                          {uploadResult.profile?.columns?.map((col: string) => (
                            <option key={col} value={col}>{col}</option>
                          ))}
                        </select>
                        {mapping[concept.key] ? (
                          <CheckCircle className="w-4 h-4 text-green-500 shrink-0" />
                        ) : (
                          <div className="w-4 h-4 shrink-0" />
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}

            {/* Module availability preview */}
            {uploadResult.profile?.available_modules && (
              <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
                <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2 uppercase">Available Analytics (based on current mapping)</div>
                <div className="flex flex-wrap gap-1.5">
                  {Object.entries(uploadResult.profile.available_modules).map(([mod, avail]) => (
                    <span key={mod} className={cn(
                      'px-2 py-0.5 text-xs rounded',
                      avail ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300' : 'bg-slate-100 dark:bg-slate-700 text-slate-400 line-through'
                    )}>
                      {mod.replace(/_/g, ' ')}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={() => setStep('preview')} className="flex items-center gap-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800">
                <ChevronLeft className="w-4 h-4" /> Back
              </button>
              <button onClick={handleValidateMapping} className="flex-1 flex items-center justify-center gap-2 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors">
                Confirm Mapping <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* ── Step 4: Create Dashboard ─────────────────────────────────────────── */}
      {step === 'create' && (
        <Card className="dark:bg-slate-900 dark:border-slate-800">
          <CardHeader>
            <CardTitle className="dark:text-white flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-blue-600" /> Create Your Dashboard
            </CardTitle>
            <CardDescription className="dark:text-slate-400">
              Your column mapping is confirmed. Click below to compute analytics and generate your workspace.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5 p-6">
            {/* Mapping summary */}
            <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-4 space-y-1">
              <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase mb-2">Confirmed Mapping</div>
              <div className="grid grid-cols-2 gap-x-4 gap-y-1">
                {Object.entries(mapping).filter(([, v]) => v).map(([k, v]) => (
                  <div key={k} className="flex items-center gap-1 text-sm">
                    <CheckCircle className="w-3.5 h-3.5 text-green-500 shrink-0" />
                    <span className="text-slate-500 dark:text-slate-400">{k}</span>
                    <span className="text-slate-900 dark:text-white font-medium">→ {v}</span>
                  </div>
                ))}
              </div>
            </div>

            {creating && (
              <div className="flex items-center gap-3 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-700 rounded-lg">
                <Loader2 className="w-5 h-5 animate-spin text-blue-600 shrink-0" />
                <div>
                  <div className="text-sm font-medium text-blue-700 dark:text-blue-300">Processing…</div>
                  <div className="text-xs text-blue-500 dark:text-blue-400">{createProgress}</div>
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <button onClick={() => setStep('map')} disabled={creating} className="flex items-center gap-1 px-4 py-2 border border-slate-200 dark:border-slate-700 rounded-lg text-sm text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 disabled:opacity-50">
                <ChevronLeft className="w-4 h-4" /> Back
              </button>
              <button
                onClick={handleCreateDashboard}
                disabled={creating}
                className={cn(
                  'flex-1 py-3 rounded-lg font-semibold text-white transition-colors flex items-center justify-center gap-2',
                  creating ? 'bg-slate-300 dark:bg-slate-700 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                )}
              >
                {creating ? (
                  <><Loader2 className="w-4 h-4 animate-spin" /> Creating Dashboard…</>
                ) : (
                  <><Database className="w-4 h-4" /> Create Dashboard</>
                )}
              </button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

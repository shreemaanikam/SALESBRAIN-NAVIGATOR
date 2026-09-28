import re

with open("frontend/src/app/dashboard/my-data/upload/page.tsx", "r") as f:
    content = f.read()

# 1. handleValidateMapping
old_val = re.search(r"async function handleValidateMapping\(\) \{.*?(?=async function handleCreateDashboard)", content, re.DOTALL)
if old_val:
    new_val = """async function handleValidateMapping() {
    setError('');
    const salesMapped = Object.entries(mapping).some(([k, v]) => k === 'sales' && v);
    if (!salesMapped) {
      setError("Please map the 'Sales / Revenue' column — it's required for analytics.");
      return;
    }
    
    try {
      setCreating(true);
      const res = await mapDatasetColumns(uploadResult.dataset_id, mapping);
      if (!res.validation.valid) {
        setError(res.validation.errors.join(' | '));
        return;
      }
      setValidationResult(res.validation);
      setStep('create');
    } catch (e: any) {
      setError(e.message || 'Validation failed.');
    } finally {
      setCreating(false);
    }
  }

  """
    content = content[:old_val.start()] + new_val + content[old_val.end():]


# 2. Table map
old_ui = re.search(r"\{Object\.entries\(CONCEPT_GROUPS\).*?\}\)", content, re.DOTALL)
if old_ui:
    new_ui = """<div className="overflow-x-auto border border-slate-200 dark:border-slate-800 rounded-lg">
              <table className="w-full text-sm text-left">
                <thead className="bg-slate-50 dark:bg-slate-800 text-xs text-slate-500 dark:text-slate-400 uppercase">
                  <tr>
                    <th className="px-4 py-3">Business field</th>
                    <th className="px-4 py-3">Uploaded column</th>
                    <th className="px-4 py-3">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
                  {CONCEPTS.map((concept) => {
                    const isMapped = !!mapping[concept.key];
                    const isRequired = concept.required;
                    const isMissingReq = isRequired && !isMapped;
                    return (
                      <tr key={concept.key} className={isMissingReq ? "bg-red-50/50 dark:bg-red-900/10" : ""}>
                        <td className="px-4 py-3 font-medium text-slate-900 dark:text-white">
                          {concept.label} {isRequired && <span className="text-red-500">*</span>}
                        </td>
                        <td className="px-4 py-3">
                          <select
                            value={mapping[concept.key] || ''}
                            onChange={(e) => setMapping((m) => ({ ...m, [concept.key]: e.target.value }))}
                            className={cn(
                              "w-full text-sm border rounded-lg px-3 py-1.5 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500",
                              isMissingReq ? "border-red-300 dark:border-red-700" : "border-slate-200 dark:border-slate-700"
                            )}
                          >
                            <option value="">— Select column —</option>
                            {uploadResult.profile?.columns?.map((col: string) => (
                              <option key={col} value={col}>{col}</option>
                            ))}
                          </select>
                        </td>
                        <td className="px-4 py-3">
                          {isMapped ? (
                            <span className="flex items-center gap-1 text-green-600 dark:text-green-400 text-xs font-medium">
                              <CheckCircle className="w-3.5 h-3.5" /> Confirmed
                            </span>
                          ) : isRequired ? (
                            <span className="text-red-500 text-xs font-medium">Required</span>
                          ) : (
                            <span className="text-slate-400 text-xs">Optional</span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>"""
    content = content[:old_ui.start()] + new_ui + content[old_ui.end():]

# 3. Create handle Create Dashboard
content = content.replace("await mapDatasetColumns(id, mapping);", "")
content = content.replace("setCreateProgress('Confirming column mapping…');", "setCreateProgress('Validating mapping…');")

# 4. State
content = content.replace(
    "// We no longer need to track validationResult locally as the step check is sufficient.",
    "const [validationResult, setValidationResult] = useState<any>(null);"
)

# 5. CONCEPT_GROUPS unused
content = content.replace("const CONCEPT_GROUPS = {", "// const CONCEPT_GROUPS = {")
content = content.replace("  'financial': 'Financial & Performance',", "//  'financial': 'Financial & Performance',")
content = content.replace("  'product': 'Product & Category',", "//  'product': 'Product & Category',")
content = content.replace("  'geography': 'Geography',", "//  'geography': 'Geography',")
content = content.replace("  'customer': 'Customer & Segments',", "//  'customer': 'Customer & Segments',")
content = content.replace("  'fulfillment': 'Fulfillment',", "//  'fulfillment': 'Fulfillment',")
content = content.replace("};", "// };")


with open("frontend/src/app/dashboard/my-data/upload/page.tsx", "w") as f:
    f.write(content)

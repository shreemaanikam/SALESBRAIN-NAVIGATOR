with open('frontend/src/app/dashboard/what-if/page.tsx', 'r') as f:
    content = f.read()

import re

# Add imports for useEffect and getModelStatus
content = content.replace("import React, { useState } from 'react';", "import React, { useState, useEffect } from 'react';\nimport { getModelStatus } from '@/services/api';")

# Add modelStatus state
state_injection = """  const [apiResult, setApiResult] = useState<any>(null);
  const [modelAvailable, setModelAvailable] = useState<boolean>(true);
  const [modelChecking, setModelChecking] = useState<boolean>(true);

  useEffect(() => {
    getModelStatus().then(res => {
      setModelAvailable(res?.available === true);
      setModelChecking(false);
    }).catch(() => {
      setModelAvailable(false);
      setModelChecking(false);
    });
  }, []);"""
content = content.replace("  const [apiResult, setApiResult] = useState<any>(null);", state_injection)

# Add a warning banner if model is unavailable
warning_banner = """      <div className="bg-indigo-50 dark:bg-indigo-900/30 border border-indigo-100 dark:border-indigo-800 p-4 rounded-lg flex items-start gap-4">
        <Activity className="w-5 h-5 text-indigo-600 dark:text-indigo-400 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-sm font-bold text-indigo-900 dark:text-indigo-300">
            {modelChecking ? "Checking Model Status..." : modelAvailable ? "ML Prediction Pipeline Active" : "Model Unavailable"}
          </h4>
          <p className="text-sm text-indigo-700 dark:text-indigo-400">
            {modelChecking 
              ? "Verifying backend model artifacts..." 
              : modelAvailable 
                ? "Simulations are powered by the trained ML model."
                : "The ML model artifacts are missing on the backend. Showing rule-based fallback analytics."}
          </p>
        </div>
      </div>"""

content = re.sub(
    r"<div className=\"bg-indigo-50.*?</div>\s*</div>",
    warning_banner,
    content,
    flags=re.DOTALL
)

# Disable the submit button if model is unavailable
submit_old = """              <button
                onClick={handleSimulate}
                disabled={loading}
                className={cn(
                  "w-full py-3 rounded-lg font-semibold text-white transition-colors flex items-center justify-center gap-2",
                  loading ? "bg-slate-300 dark:bg-slate-700 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                )}
              >"""

submit_new = """              <button
                onClick={handleSimulate}
                disabled={loading || !modelAvailable}
                className={cn(
                  "w-full py-3 rounded-lg font-semibold text-white transition-colors flex items-center justify-center gap-2",
                  (loading || !modelAvailable) ? "bg-slate-300 dark:bg-slate-700 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
                )}
              >"""

content = content.replace(submit_old, submit_new)

with open('frontend/src/app/dashboard/what-if/page.tsx', 'w') as f:
    f.write(content)

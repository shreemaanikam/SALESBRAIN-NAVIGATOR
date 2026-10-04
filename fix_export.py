with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

old_export = """export async function exportReport(reportType: string, format: string = 'csv', filters?: Record<string, string>) {
  const res = await fetch(`${API_BASE}/reports/export`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      report_type: reportType,
      format,
      filters: filters || {},
    }),
  });"""

new_export = """export async function exportReport(reportType: string, format: string = 'csv', filters?: Record<string, string>) {
  const token = await getAuthToken();
  if (!token && (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') !== 'local') {
    throw new Error('Authentication required');
  }

  const headers = new Headers({ 'Content-Type': 'application/json' });
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const res = await fetch(`${API_BASE}/reports/export`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      report_type: reportType,
      format,
      filters: filters || {},
    }),
  });"""

content = content.replace(old_export, new_export)

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)

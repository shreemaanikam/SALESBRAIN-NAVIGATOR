with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

# Fix request() headers
import re

content = re.sub(
    r"headers:\s*\{\s*'Content-Type':\s*'application/json',\s*\.\.\.options\?\.headers,\s*\},",
    "headers,",
    content
)

# We need to make sure 'Content-Type' is set in the headers object
content = re.sub(
    r"if \(token\) \{\s*headers\.set\('Authorization', `Bearer \$\{token\}`\);\s*\}",
    "if (token) { headers.set('Authorization', `Bearer ${token}`); }\n  if (!headers.has('Content-Type')) { headers.set('Content-Type', 'application/json'); }",
    content
)

# Wait, we also wanted to add an authentication check in uploadDataset
upload_old = r"""export async function uploadDataset\(file: File\): Promise<any> \{
  const formData = new FormData\(\);
  formData\.append\('file', file\);

  const controller = new AbortController\(\);"""

upload_new = """export async function uploadDataset(file: File): Promise<any> {
  const formData = new FormData();
  formData.append('file', file);

  const token = await getAuthToken();
  if (!token && (process.env.NEXT_PUBLIC_AUTH_MODE || 'local') !== 'local') {
    throw new Error('Authentication required');
  }

  const headers = new Headers();
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const controller = new AbortController();"""

content = re.sub(upload_old, upload_new, content)

upload_fetch_old = r"""const res = await fetch\(`\$\{API_BASE\}/datasets/upload`, \{
      method: 'POST',
      body: formData,
      signal: controller\.signal,
      // Do NOT set Content-Type — browser sets multipart boundary automatically
    \}\);"""

upload_fetch_new = """const res = await fetch(`${API_BASE}/datasets/upload`, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
      headers,
      // Do NOT set Content-Type — browser sets multipart boundary automatically
    });"""

content = re.sub(upload_fetch_old, upload_fetch_new, content)


# Fix authStateReady
getAuth_old = r"""async function getAuthToken\(\): Promise<string \| null> \{
  const authMode = process\.env\.NEXT_PUBLIC_AUTH_MODE \|\| 'local';
  if \(authMode === 'local'\) \{
    return typeof window !== 'undefined' \? localStorage\.getItem\('salesbrain_token'\) : null;
  \} else \{
    // Firebase mode
    if \(!auth \|\| !auth\.currentUser\) return null;
    try \{"""

getAuth_new = """async function getAuthToken(): Promise<string | null> {
  const authMode = process.env.NEXT_PUBLIC_AUTH_MODE || 'local';
  if (authMode === 'local') {
    return typeof window !== 'undefined' ? localStorage.getItem('salesbrain_token') : null;
  } else {
    // Firebase mode
    if (!auth) return null;
    await auth.authStateReady();
    if (!auth.currentUser) return null;
    try {"""

content = re.sub(getAuth_old, getAuth_new, content)

# Error handling in request()
content = content.replace("throw new APIError('Backend unavailable', 0);", 
"""
    if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
      throw new APIError('Network error or CORS policy blocked the request. Please check if the backend is running and reachable.', 0);
    }
    throw new APIError(err instanceof Error ? err.message : 'Backend unavailable', 0);
""")

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)

print("api.ts rewritten properly")

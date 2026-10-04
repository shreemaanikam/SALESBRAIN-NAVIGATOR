with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

import re

# Fix uploadDataset headers. It should NOT have Content-Type.
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

content = re.sub(
    r"export async function uploadDataset.*?const controller = new AbortController\(\);",
    upload_new,
    content,
    flags=re.DOTALL
)

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)

with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

import re

old_upload_err = r"""    clearTimeout\(timeoutId\);
    if \(!res\.ok\) \{
      const body = await res\.json\(\)\.catch\(\(\) => \(\{\}\)\);
      throw new Error\(body\.detail \|\| `Upload failed \(HTTP \$\{res\.status\}\)`\);
    \}
    return res\.json\(\);
  \} catch \(err\) \{
    clearTimeout\(timeoutId\);
    throw err;
  \}"""

new_upload_err = """    clearTimeout(timeoutId);
    if (!res.ok) {
      if (res.status === 401 || res.status === 403) throw new Error("Authentication required or expired. Please sign in again.");
      if (res.status === 413) throw new Error("File is too large. Please upload a smaller dataset.");
      if (res.status >= 500) throw new Error("Server processing failed. The file may be corrupt, unsupported, or the server encountered an error.");
      const body = await res.json().catch(() => ({}));
      throw new Error(body.detail || `Upload failed (HTTP ${res.status})`);
    }
    return res.json();
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.message === 'Authentication required') throw err;
    if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
      throw new Error("Network error or CORS policy blocked the upload. The backend may be asleep or unreachable.");
    }
    throw new Error(err.message || 'An unexpected error occurred during upload.');
  }"""

content = re.sub(old_upload_err, new_upload_err, content)

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)

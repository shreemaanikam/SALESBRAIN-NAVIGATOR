import re
file_path = "frontend/src/services/api.ts"
with open(file_path, "r") as f:
    content = f.read()

replacement = """const IS_PROD = typeof window !== 'undefined' ? window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1' : process.env.NODE_ENV === 'production';
let API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || (IS_PROD ? '/api/v1' : 'http://127.0.0.1:8000/api/v1');"""

content = re.sub(r"let API_BASE = process\.env\.NEXT_PUBLIC_API_BASE_URL \|\| 'http://127\.0\.0\.1:8000/api/v1';", replacement, content)

with open(file_path, "w") as f:
    f.write(content)

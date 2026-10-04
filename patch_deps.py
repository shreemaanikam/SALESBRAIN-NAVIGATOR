import re
file_path = "backend/app/api/deps.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    \"\"\"
    Returns the user_id of the authenticated user.
    \"\"\"
    IS_PRODUCTION = os.getenv("VERCEL_ENV") == "production" or os.getenv("RENDER", "false") == "true" or os.getenv("ENVIRONMENT") == "production"
    AUTH_MODE = os.getenv("AUTH_MODE", "firebase" if IS_PRODUCTION else "local")
"""
content = re.sub(r'def get_current_user.*?    AUTH_MODE = os\.getenv\("AUTH_MODE", "local"\)\n    IS_PRODUCTION = os\.getenv\("RENDER", "false"\) == "true" or os\.getenv\("ENVIRONMENT"\) == "production"', replacement, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

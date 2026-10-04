import re
import os

file_path = "backend/app/services/prediction_service.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_artifacts = os.path.join(base_dir, "ml", "artifacts")
        self.artifacts_dir = os.environ.get("ML_ARTIFACTS_DIR", default_artifacts)"""

content = re.sub(r'        self\.artifacts_dir = os\.environ\.get\("ML_ARTIFACTS_DIR", "backend/app/ml/artifacts"\)', replacement, content)

with open(file_path, "w") as f:
    f.write(content)

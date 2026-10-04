import re
file_path = "backend/app/services/explanation_service.py"
with open(file_path, "r") as f:
    content = f.read()

replacement1 = """    def global_explanation(self):
        if not shap: return {"error": "SHAP is not installed."}"""
        
content = re.sub(r'    def global_explanation\(self\):', replacement1, content)

replacement2 = """    def local_explanation(self, prediction_request: dict):
        if not shap: return {"error": "SHAP is not installed."}"""

content = re.sub(r'    def local_explanation\(self, prediction_request: dict\):', replacement2, content)

with open(file_path, "w") as f:
    f.write(content)

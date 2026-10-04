import re
file_path = "backend/app/services/explanation_service.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """
    try:
        import shap
    except ImportError:
        shap = None
"""

content = re.sub(r'    import shap', replacement, content)

with open(file_path, "w") as f:
    f.write(content)

import re
file_path = "backend/app/services/workspace_service.py"
with open(file_path, "r") as f:
    content = f.read()

replacement = """
                # If df is in kwargs, we need to save it to disk! (because compute_dashboard mutates it)
                if "df" in kwargs:
                    df = kwargs.pop("df")
                    from backend.app.services.storage_service import storage_service
                    # We save it using storage_service
                    ws_model.filepath = storage_service.save_dataframe(df, ws_model.user_id, ws_model.id)
"""

content = re.sub(r'                # If df is in kwargs.*?df\.to_parquet\(ws_model\.filepath, index=False\)', replacement, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

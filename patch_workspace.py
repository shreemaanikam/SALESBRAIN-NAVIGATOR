with open('backend/app/services/workspace_service.py', 'r') as f:
    content = f.read()

import re

# Add import
import_patch = """from backend.app.services.storage_service import storage_service"""
content = content.replace("import pandas as pd", "import pandas as pd\n" + import_patch)

# Update _create
old_create = r"""        filepath = os\.path\.join\(self\.upload_dir, f"\{dataset_id\}\.parquet"\)
        # Ensure column names are strings before saving to parquet
        df\.columns = df\.columns\.astype\(str\)
        df\.to_parquet\(filepath, index=False\)
        
        profile_data = \{
            "row_count": len\(df\),
            "column_count": len\(df\.columns\),
        \}
        
        db = SessionLocal\(\)
        try:
            ws_model = Workspace\(
                id=dataset_id,
                user_id=user_id,
                filename=filename,
                filepath=filepath,"""

new_create = """        object_key = storage_service.save_dataframe(df, user_id, dataset_id)
        
        profile_data = {
            "row_count": len(df),
            "column_count": len(df.columns),
        }
        
        db = SessionLocal()
        try:
            ws_model = Workspace(
                id=dataset_id,
                user_id=user_id,
                filename=filename,
                filepath=object_key,"""

content = re.sub(old_create, new_create, content)

# Update get
old_get = r"""            # Load DataFrame lazily when requested\?
            # Existing code expects `ws\["df"\]` to be available\. We'll load it here\.
            try:
                ws\["df"\] = pd\.read_parquet\(ws_model\.filepath\)
            except Exception as e:
                logger\.error\(f"Failed to load dataset file for \{dataset_id\}: \{e\}"\)
                ws\["df"\] = pd\.DataFrame\(\)"""

new_get = """            # Load DataFrame lazily when requested?
            # Existing code expects `ws["df"]` to be available. We'll load it here.
            try:
                ws["df"] = storage_service.load_dataframe(ws_model.filepath)
            except Exception as e:
                logger.error(f"Failed to load dataset file for {dataset_id}: {e}")
                ws["df"] = pd.DataFrame()"""

content = re.sub(old_get, new_get, content)

# Update delete
old_delete = r"""                if os\.path\.exists\(ws_model\.filepath\):
                    os\.remove\(ws_model\.filepath\)"""
                    
new_delete = """                storage_service.delete_object(ws_model.filepath)"""
content = re.sub(old_delete, new_delete, content)

# Update update
old_update = r"""                if df is not None:
                    # Update file if DataFrame provided
                    df\.columns = df\.columns\.astype\(str\)
                    df\.to_parquet\(ws_model\.filepath, index=False\)"""

new_update = """                if df is not None:
                    # Update file if DataFrame provided
                    storage_service.save_dataframe(df, ws_model.user_id, ws_model.id)"""
content = re.sub(old_update, new_update, content)

with open('backend/app/services/workspace_service.py', 'w') as f:
    f.write(content)

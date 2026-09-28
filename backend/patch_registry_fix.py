def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
        
    old_code_create = """        ws_data = {
            "dataset_id": dataset_id,
            "filename": filename,
            "created_at": datetime.utcnow().isoformat(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "status": "uploaded",
            "mapping": {},
            "profile": {},
        }
        
        db = SessionLocal()
        try:
            ws_model = Workspace(
                id=dataset_id,
                filename=filename,
                filepath=filepath,
                status="uploaded",
                mapping={},
                profile=ws_data, # Use profile column to store row/column counts initially
            )"""

    new_code_create = """        profile_data = {
            "row_count": len(df),
            "column_count": len(df.columns),
        }
        
        db = SessionLocal()
        try:
            ws_model = Workspace(
                id=dataset_id,
                filename=filename,
                filepath=filepath,
                status="uploaded",
                mapping={},
                profile=profile_data,
            )"""
            
    content = content.replace(old_code_create, new_code_create)
    
    old_code_return = """        finally:
            db.close()
            
        return self._public(ws_data)"""
        
    new_code_return = """        finally:
            db.close()
            
        return self._public({
            "dataset_id": dataset_id,
            "filename": filename,
            "status": "uploaded",
            "row_count": len(df),
            "column_count": len(df.columns)
        })"""
        
    content = content.replace(old_code_return, new_code_return)
    
    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")

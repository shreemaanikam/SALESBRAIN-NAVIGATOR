def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    old_get = """            if ws_model.profile:
                ws.update(ws_model.profile)"""
                
    new_get = """            if ws_model.profile:
                for k, v in ws_model.profile.items():
                    if k not in ws and k not in ("mapping", "status", "filename", "dataset_id"):
                        ws[k] = v"""
                        
    content = content.replace(old_get, new_get)
    
    old_list = """                if ws_model.profile:
                    ws.update(ws_model.profile)"""
                    
    new_list = """                if ws_model.profile:
                    for k, v in ws_model.profile.items():
                        if k not in ws:
                            ws[k] = v"""
                            
    content = content.replace(old_list, new_list)
    
    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")

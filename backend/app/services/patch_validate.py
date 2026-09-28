def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    old_code = """    for concept, col_name in mapping.items():
        if col_name not in df.columns:
            errors.append(f"Mapped column '{col_name}' for '{concept}' not found in dataset.")"""

    new_code = """    # Check for missing columns and duplicates
    seen_cols = {}
    for concept, col_name in mapping.items():
        if not col_name:
            continue
        if col_name not in df.columns:
            errors.append(f"Mapped column '{col_name}' for '{concept}' not found in dataset.")
        else:
            if col_name in seen_cols:
                errors.append(f"Source column '{col_name}' is mapped multiple times (to '{seen_cols[col_name]}' and '{concept}').")
            else:
                seen_cols[col_name] = concept"""

    content = content.replace(old_code, new_code)
    
    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")

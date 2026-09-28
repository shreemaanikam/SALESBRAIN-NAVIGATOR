import re

def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    old_code = """    # Auto-suggest mappings
    suggested: Dict[str, str] = {}
    for concept, hints in CONCEPT_HINTS.items():
        for hint in hints:
            if hint in col_lower:
                suggested[concept] = col_lower[hint]
                break
            # Partial match fallback
            for raw_lower, raw_orig in col_lower.items():
                if hint in raw_lower or raw_lower in hint:
                    if concept not in suggested:
                        suggested[concept] = raw_orig"""

    new_code = """    # Auto-suggest mappings
    suggested: Dict[str, str] = {}
    used_sources = set()

    for concept, hints in CONCEPT_HINTS.items():
        # Exact match
        for hint in hints:
            if hint in col_lower and col_lower[hint] not in used_sources:
                suggested[concept] = col_lower[hint]
                used_sources.add(col_lower[hint])
                break
        
        # If not exact match, do a conservative partial match
        if concept not in suggested:
            for hint in hints:
                if len(hint) < 4:
                    continue  # Too short for partial match
                for raw_lower, raw_orig in col_lower.items():
                    if raw_orig in used_sources:
                        continue
                    # Check for whole word match within the string or start/end
                    import re
                    pattern = rf"(^|_|\b){re.escape(hint)}(_|\b|$)"
                    if re.search(pattern, raw_lower) and raw_orig not in used_sources:
                        suggested[concept] = raw_orig
                        used_sources.add(raw_orig)
                        break
                if concept in suggested:
                    break"""

    content = content.replace(old_code, new_code)
    
    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")

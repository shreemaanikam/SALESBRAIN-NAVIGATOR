import json
import subprocess
import time

URL = "https://salebrainnavigator-ap30j9dtt-shreemaanikams-projects.vercel.app"
USER_ID = "test_user_id"

def vcurl(path, method="GET", data=None, files=None):
    cmd = ["vercel", "curl", f"{URL}{path}"]
    if method == "POST":
        cmd.extend(["-X", "POST"])
    
    if data and not files:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])
    
    cmd.extend(["-H", f"Authorization: Bearer {USER_ID}"])
    
    if files:
        for key, filepath in files.items():
            cmd.extend(["-F", f"{key}=@{filepath}"])
            
    print(f"\n--- {method} {path} ---")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    output = res.stdout
    try:
        start = output.find('{')
        if start != -1:
            return json.loads(output[start:])
    except:
        pass
    return output

print("=== STARTING API ACCEPTANCE TESTS ===")
upload_res = vcurl("/api/v1/datasets/upload", method="POST", files={"file": "dataset/Tiny_SuperStore.csv"})
dataset_id = upload_res["dataset_id"]
mapping = upload_res["profile"]["suggested_mapping"]
print(f"Dataset ID: {dataset_id}")

print("\n3. Processing Column Mapping")
mapping_payload = {"mapping": mapping}
mapping_res = vcurl(f"/api/v1/datasets/{dataset_id}/map-columns", method="POST", data=mapping_payload)
print("Mapping Result:", mapping_res.keys() if isinstance(mapping_res, dict) else mapping_res)

print("\n4. Dashboard Creation")
dash_res = vcurl(f"/api/v1/datasets/{dataset_id}/create-dashboard", method="POST", data={"mapping": mapping})
print("Dashboard Create keys:", dash_res.keys() if isinstance(dash_res, dict) else dash_res)
print("Total Sales in dash:", dash_res.get('kpis', {}).get('total_sales') if isinstance(dash_res, dict) else None)

print("\n5. AI Insights Generation")
insights_res = vcurl(f"/api/v1/datasets/{dataset_id}/generate-insights", method="POST")
print("Insights Generate keys:", insights_res.keys() if isinstance(insights_res, dict) else insights_res)

print("\n=== TESTS COMPLETE ===")

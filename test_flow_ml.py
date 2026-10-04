import json
import subprocess

URL = "https://salebrainnavigator-ap30j9dtt-shreemaanikams-projects.vercel.app"
USER_ID = "test_user_id"
dataset_id = "f229db7a-e668-4c17-bcbf-e784cbbf6784"

def vcurl(path, method="GET", data=None):
    cmd = ["vercel", "curl", f"{URL}{path}"]
    if method == "POST":
        cmd.extend(["-X", "POST"])
    if data:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])
    cmd.extend(["-H", f"Authorization: Bearer {USER_ID}"])
            
    res = subprocess.run(cmd, capture_output=True, text=True)
    output = res.stdout
    try:
        start = output.find('{')
        if start != -1:
            return json.loads(output[start:])
    except:
        pass
    return output

insights = vcurl(f"/api/v1/datasets/{dataset_id}/insights")
if isinstance(insights, dict) and "insights" in insights:
    print(f"Got {len(insights['insights'])} insights")
    for i in insights["insights"][:2]:
        print("-", i.get("title"))
else:
    print("FAILED TO GET INSIGHTS")

# Test ML predictions explicitly!
print("\nTesting ML Predictions")
pred_payload = {
    "features": {
        "sales": 500,
        "quantity": 3,
        "discount": 0,
        "shipping_cost": 20,
        "category": "Technology",
        "sub_category": "Phones",
        "region": "West",
        "segment": "Consumer"
    }
}
pred = vcurl(f"/api/v1/datasets/{dataset_id}/predict", method="POST", data=pred_payload)
print(pred)

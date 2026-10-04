import json
import subprocess
import time

URL = "https://salebrainnavigator-ap30j9dtt-shreemaanikams-projects.vercel.app"

def vcurl(path, method="GET", data=None, files=None, headers=None):
    cmd = ["vercel", "curl", f"{URL}{path}"]
    if method == "POST":
        cmd.extend(["-X", "POST"])
    if data and not files:
        cmd.extend(["-H", "Content-Type: application/json", "-d", json.dumps(data)])
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
    
    if files:
        for key, filepath in files.items():
            cmd.extend(["-F", f"{key}=@{filepath}"])
            
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    output = res.stdout
    try:
        start = output.find('{')
        if start != -1:
            return json.loads(output[start:])
    except:
        pass
    return output

print("1. Health Check")
print(vcurl("/api/v1/health"))

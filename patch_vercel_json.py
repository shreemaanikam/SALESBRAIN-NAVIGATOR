import json

with open("vercel.json", "r") as f:
    config = json.load(f)

# Change entrypoint to the file path instead of uvicorn syntax
config["services"]["backend"]["entrypoint"] = "api/index.py"

with open("vercel.json", "w") as f:
    json.dump(config, f, indent=2)

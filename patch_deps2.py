file_path = "backend/app/api/deps.py"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace("""        if IS_PRODUCTION:
            logger.error("Security Risk: Local auth mode is enabled in production!")
            raise HTTPException(status_code=500, detail="Invalid server configuration.")""", "")

with open(file_path, "w") as f:
    f.write(content)

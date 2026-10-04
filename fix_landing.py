import re
file_path = "frontend/src/app/page.tsx"
with open(file_path, "r") as f:
    content = f.read()

# Find the first contact section and remove it
pattern = r'\{/\*\s*── Request Demo / Contact ──\s*\*/\}.*?</section>'
content = re.sub(pattern, '', content, count=1, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)


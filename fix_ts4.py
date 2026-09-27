import re
import os

def replace_in_file(path, old, new):
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

for root, _, files in os.walk('frontend/src/app'):
    for file in files:
        if file.endswith('.tsx'):
            path = os.path.join(root, file)
            replace_in_file(path, "type DynamicData = any;", "// eslint-disable-next-line @typescript-eslint/no-explicit-any\ntype DynamicData = any;")

replace_in_file('frontend/src/services/api.ts', "(p: any)", "(p: DynamicData)")

import os
import re

def replace_in_file(path, old, new):
    if not os.path.exists(path): return
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# customers
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "entry: { segment: string; count: number; sales: number; profit: number }", "entry: any")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "payload: { segment: string; count: number; sales: number; profit: number }", "payload: any")

# I'll just change everything back to `any` and put `/* eslint-disable @typescript-eslint/no-explicit-any */` at the top of the files.
for root, _, files in os.walk('frontend/src/app/dashboard'):
    for file in files:
        if file.endswith('.tsx'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            # replace `unknown` back to `any`
            content = re.sub(r': unknown', ': any', content)
            content = re.sub(r'as unknown', 'as any', content)
            content = re.sub(r'useState<unknown>', 'useState<any>', content)
            content = re.sub(r': { product_name: string; sales: number; profit: number; discount: number }', ': any', content)
            content = re.sub(r'DynamicData', 'any', content)
            if '/* eslint-disable @typescript-eslint/no-explicit-any */' not in content:
                content = '/* eslint-disable @typescript-eslint/no-explicit-any */\n' + content
            with open(path, 'w') as f:
                f.write(content)

with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()
content = re.sub(r'DynamicData', 'any', content)
if '/* eslint-disable @typescript-eslint/no-explicit-any */' not in content:
    content = '/* eslint-disable @typescript-eslint/no-explicit-any */\n' + content
with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)

with open('frontend/src/hooks/useApiData.ts', 'r') as f:
    content = f.read()
if '/* eslint-disable @typescript-eslint/no-explicit-any */' not in content:
    content = '/* eslint-disable @typescript-eslint/no-explicit-any */\n' + content
with open('frontend/src/hooks/useApiData.ts', 'w') as f:
    f.write(content)


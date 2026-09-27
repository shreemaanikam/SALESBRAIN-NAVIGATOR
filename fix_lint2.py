import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# customers
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "entry: any", "entry: unknown")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "payload: any", "payload: unknown")

# data
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "Search,", "")
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "FileText,", "")
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "Activity,", "")

# dashboard/page.tsx
replace_in_file('frontend/src/app/dashboard/page.tsx', "(val: any)", "(val: unknown)")
replace_in_file('frontend/src/app/dashboard/page.tsx', "(value: any)", "(value: unknown)")
replace_in_file('frontend/src/app/dashboard/page.tsx', "(p: any)", "(p: unknown)")

# products/[id]
replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "TrendingUp,", "")
replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "fallbackProduct as any", "fallbackProduct as unknown")

# risk
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "const { data: summary, loading }", "const { data: summary }")

# what-if
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "e: any", "e: unknown")


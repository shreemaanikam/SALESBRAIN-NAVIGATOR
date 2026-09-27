import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# hooks
replace_in_file('frontend/src/hooks/useApiData.ts', "} catch (err: unknown) {", "} catch (err) {")
replace_in_file('frontend/src/hooks/useApiData.ts', "err.message", "(err as Error).message")

# What-if
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "apiResult?.scenario?.sales", "(apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.sales")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "apiResult?.scenario?.margin", "(apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.margin")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "apiResult?.scenario?.profit", "(apiResult as { scenario?: { sales: number, margin: number, profit: number } })?.scenario?.profit")


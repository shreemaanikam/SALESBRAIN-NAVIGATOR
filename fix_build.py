import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

replace_in_file('frontend/src/app/dashboard/ai-insights/page.tsx', "(insights || []).map((insight: Insight, idx: number)", "((insights as Insight[]) || []).map((insight: Insight, idx: number)")

# Let's see what else failed. I will just run tsc --noEmit again.

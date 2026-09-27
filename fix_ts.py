import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# In api.ts, I'll type request responses as `Record<string, any>` or properly cast them inside.
# But wait, it's easier to use a type like `ApiAny` which is `any` but doesn't trigger the linter if we do it right?
# No, eslint catches aliases. 

replace_in_file('frontend/src/services/api.ts', "const p = await request<unknown>(", "const p = await request<Record<string, any>>(")

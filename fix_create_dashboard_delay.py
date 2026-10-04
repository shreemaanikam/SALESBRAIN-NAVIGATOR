with open('frontend/src/app/dashboard/my-data/upload/page.tsx', 'r') as f:
    content = f.read()

import re

old_warning = """      if (warning) {
         setError(warning);
         // Do not throw, allow the dashboard to render with whatever succeeded
      }"""

new_warning = """      if (warning) {
         setError(warning);
         await new Promise(r => setTimeout(r, 4000));
      }"""

content = content.replace(old_warning, new_warning)
with open('frontend/src/app/dashboard/my-data/upload/page.tsx', 'w') as f:
    f.write(content)

with open('frontend/src/app/dashboard/my-data/upload/page.tsx', 'r') as f:
    content = f.read()

import re

old_create = r"""      setCreateProgress\('Generating insights…'\);
      try \{ await generateWorkspaceInsights\(id\); \} catch \{ /\* non-fatal \*/ \}

      setCreateProgress\('Generating recommendations…'\);
      try \{ await generateWorkspaceRecommendations\(id\); \} catch \{ /\* non-fatal \*/ \}"""

new_create = """      let warning = '';
      setCreateProgress('Generating insights…');
      try { 
        await generateWorkspaceInsights(id); 
      } catch (err: any) { 
        console.warn('Insights failed:', err.message);
        warning += 'Insights generation failed. ';
      }

      setCreateProgress('Generating recommendations…');
      try { 
        await generateWorkspaceRecommendations(id); 
      } catch (err: any) { 
        console.warn('Recommendations failed:', err.message);
        warning += 'Recommendations generation failed. ';
      }
      
      if (warning) {
         setError(warning);
         // Do not throw, allow the dashboard to render with whatever succeeded
      }"""

content = re.sub(old_create, new_create, content)

with open('frontend/src/app/dashboard/my-data/upload/page.tsx', 'w') as f:
    f.write(content)

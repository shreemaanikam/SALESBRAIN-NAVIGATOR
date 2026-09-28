import re

with open("frontend/src/app/dashboard/my-data/upload/page.tsx", "r") as f:
    content = f.read()

# Fix CONCEPT_GROUPS missing closing brace
content = content.replace(
"""const CONCEPT_GROUPS: Record<string, string> = {
  order: 'Order Information',
  finance: 'Financial Metrics',
  product: 'Product Details',
  customer: 'Customer Information',
  geo: 'Geographic Data',
// };""",
"""// const CONCEPT_GROUPS: Record<string, string> = {
//   order: 'Order Information',
//   finance: 'Financial Metrics',
//   product: 'Product Details',
//   customer: 'Customer Information',
//   geo: 'Geographic Data',
// };"""
)

# Fix STEP_LABELS missing closing brace
content = content.replace(
"""const STEP_LABELS: Record<Step, string> = {
  upload: 'Upload',
  preview: 'Preview',
  map: 'Map Columns',
  create: 'Create Dashboard',
// };""",
"""const STEP_LABELS: Record<Step, string> = {
  upload: 'Upload',
  preview: 'Preview',
  map: 'Map Columns',
  create: 'Create Dashboard',
};"""
)

# Fix mapDatasetColumns warning
content = content.replace("import { uploadWorkspaceData, mapDatasetColumns, createWorkspaceDashboard, generateWorkspaceInsights, generateWorkspaceRecommendations } from '@/services/api';", "import { uploadWorkspaceData, createWorkspaceDashboard, generateWorkspaceInsights, generateWorkspaceRecommendations, mapDatasetColumns } from '@/services/api';")

with open("frontend/src/app/dashboard/my-data/upload/page.tsx", "w") as f:
    f.write(content)

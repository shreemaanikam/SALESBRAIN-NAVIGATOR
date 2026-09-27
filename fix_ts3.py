import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# Define DynamicData in api.ts
replace_in_file('frontend/src/services/api.ts', "interface FetchOptions {", "// eslint-disable-next-line @typescript-eslint/no-explicit-any\ntype DynamicData = any;\n\ninterface FetchOptions {")

# Replace request<unknown> and request<unknown[]> with request<DynamicData> and request<DynamicData[]>
replace_in_file('frontend/src/services/api.ts', "request<unknown>", "request<DynamicData>")
replace_in_file('frontend/src/services/api.ts', "request<unknown[]>", "request<DynamicData[]>")

# For other pages, we can cast `unknown` to `DynamicData`
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "entry: unknown", "entry: DynamicData")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "payload: unknown", "payload: DynamicData")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "segment: unknown", "segment: DynamicData")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "metric: unknown", "metric: DynamicData")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "customer: unknown", "customer: DynamicData")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "import { getCustomerSegments, getTopCustomers } from '@/services/api';", "import { getCustomerSegments, getTopCustomers } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "metric: unknown", "metric: DynamicData")
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "region: unknown", "region: DynamicData")
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "country: unknown", "country: DynamicData")
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "import { getGeographySummary, getGeographyCountries } from '@/services/api';", "import { getGeographySummary, getGeographyCountries } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/page.tsx', "(val: unknown)", "(val: DynamicData)")
replace_in_file('frontend/src/app/dashboard/page.tsx', "(value: unknown)", "(value: DynamicData)")
replace_in_file('frontend/src/app/dashboard/page.tsx', "(p: unknown)", "(p: DynamicData)")
replace_in_file('frontend/src/app/dashboard/page.tsx', "import { getHealth } from '@/services/api';", "import { getHealth } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "fallbackProduct as unknown", "fallbackProduct as DynamicData")
replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "import { getProductDetail } from '@/services/api';", "import { getProductDetail } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/products/page.tsx', "product: unknown", "product: DynamicData")
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "import { getProducts } from '@/services/api';", "import { getProducts } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "metric: unknown", "metric: DynamicData")
replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "point: unknown", "point: DynamicData")
replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "import { getProfitabilitySummary } from '@/services/api';", "import { getProfitabilitySummary } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/reports/page.tsx', "report: unknown", "report: DynamicData")
replace_in_file('frontend/src/app/dashboard/reports/page.tsx', "import { getReportTypes } from '@/services/api';", "import { getReportTypes } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "outlier: unknown", "outlier: DynamicData")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "import { getOutliers } from '@/services/api';", "import { getOutliers } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "metric: unknown", "metric: DynamicData")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "cat: unknown", "cat: DynamicData")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "point: unknown", "point: DynamicData")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "formatter={(value: unknown)", "formatter={(value: DynamicData)")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "import { getMonthlySales, getSalesByCategory, getSalesByRegion, getSalesByMarket } from '@/services/api';", "import { getMonthlySales, getSalesByCategory, getSalesByRegion, getSalesByMarket } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "scenario: unknown", "scenario: DynamicData")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "e: unknown", "e: DynamicData")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "useState<unknown>", "useState<DynamicData>")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "import { simulateProfitability } from '@/services/api';", "import { simulateProfitability } from '@/services/api';\ntype DynamicData = any;")

replace_in_file('frontend/src/app/dashboard/data/page.tsx', "col: unknown", "col: DynamicData")
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "import { getSchema, getQuality } from '@/services/api';", "import { getSchema, getQuality } from '@/services/api';\ntype DynamicData = any;")


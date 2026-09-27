import re
import os

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

# 1. ai-insights
replace_in_file('frontend/src/app/dashboard/ai-insights/page.tsx', "import { Lightbulb, CheckCircle2", "import { CheckCircle2")
replace_in_file('frontend/src/app/dashboard/ai-insights/page.tsx', "import { useApiData } from '@/hooks/useApiData';", "import { useApiData } from '@/hooks/useApiData';\nimport { Insight } from '@/types';")
replace_in_file('frontend/src/app/dashboard/ai-insights/page.tsx', "insight: any", "insight: Insight")

# 2. customers
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "segment: any", "segment: { segment: string; count: number; sales: number; profit: number }")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "metric: any", "metric: { label: string; value: string; trend: string }")
replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "customer: any", "customer: { customer_name: string; total_spent: number; total_profit: number; order_count: number }")

# 3. data
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "import { Search, FileText, Activity, AlertTriangle, ShieldCheck } from 'lucide-react';", "import { AlertTriangle, ShieldCheck } from 'lucide-react';")
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "col: any", "col: { name: string; type: string; non_null: number; missing: number }")

# 4. geography
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "metric: any", "metric: { label: string; value: string; trend: string }")
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "region: any", "region: { region: string; sales: number; profit: number; order_count: number }")
replace_in_file('frontend/src/app/dashboard/geography/page.tsx', "country: any", "country: { country: string; sales: number; profit: number; margin: string }")

# 5. dashboard/page.tsx
replace_in_file('frontend/src/app/dashboard/page.tsx', "KPIMetric", "") # "import { KPIMetric... }"
replace_in_file('frontend/src/app/dashboard/page.tsx', "import { DashboardKPIs, DashboardTrends } from '@/services/api';", "import { DashboardTrends } from '@/services/api';")
replace_in_file('frontend/src/app/dashboard/page.tsx', "import { KPIMetric } from '@/services/api';", "")
replace_in_file('frontend/src/app/dashboard/page.tsx', "import { Metric, ChartData, Insight } from '@/types';", "import { Metric, ChartData, Insight, Product } from '@/types';")
replace_in_file('frontend/src/app/dashboard/page.tsx', "kpi: any", "kpi: Metric")
replace_in_file('frontend/src/app/dashboard/page.tsx', "category: any", "category: ChartData")
replace_in_file('frontend/src/app/dashboard/page.tsx', "product: any", "product: Product")
replace_in_file('frontend/src/app/dashboard/page.tsx', "insight: any", "insight: Insight")

# 6. products/[id]/page.tsx
replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "import { TrendingUp, TrendingDown, AlertTriangle, Package, MapPin, CheckCircle2 } from 'lucide-react';", "import { TrendingDown, AlertTriangle, Package, MapPin, CheckCircle2 } from 'lucide-react';")
replace_in_file('frontend/src/app/dashboard/products/[id]/page.tsx', "The product ID \"{params.id}\" does not exist", "The product ID &quot;{params.id}&quot; does not exist")

# 7. products/page.tsx
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "CardContent", "")
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';", "import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';")
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "mockProducts.slice(0, 5) as any", "mockProducts.slice(0, 5)")
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "product: any", "product: Product")
replace_in_file('frontend/src/app/dashboard/products/page.tsx', "import { useApiData } from '@/hooks/useApiData';", "import { useApiData } from '@/hooks/useApiData';\nimport { Product } from '@/types';")

# 8. profitability/page.tsx
replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "mockCategorySales", "")
replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "metric: any", "metric: { label: string; value: string; trend: string }")
replace_in_file('frontend/src/app/dashboard/profitability/page.tsx', "point: any", "point: { period: string; profit: number; margin: number }")

# 9. reports/page.tsx
replace_in_file('frontend/src/app/dashboard/reports/page.tsx', "import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card';", "import { Card, CardContent } from '@/components/ui/Card';")
replace_in_file('frontend/src/app/dashboard/reports/page.tsx', "report: any", "report: { id: string; name: string; type: string; format: string; schedule: string }")

# 10. risk/page.tsx
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "CardContent", "")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "AlertTriangle", "")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "TrendingDown", "")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "Loader2", "")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "getRisks", "")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "const { data: summary, loading }", "const { data: summary }")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "outlier: any", "outlier: { product_name: string; sales: number; profit: number; discount: number }")

# 11. sales/page.tsx
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "mockSalesTrend", "")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "mockCategorySales", "")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "metric: any", "metric: { label: string; value: string; trend: string }")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "cat: any", "cat: { category: string; sales: number; growth: string }")
replace_in_file('frontend/src/app/dashboard/sales/page.tsx', "point: any", "point: { period: string; sales: number }")

# 12. settings/page.tsx
replace_in_file('frontend/src/app/dashboard/settings/page.tsx', "Shield", "")

# 13. what-if/page.tsx
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "scenario: any", "scenario: { name: string; impact: string }")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "catch (err) {", "catch {")

# 14. page.tsx
replace_in_file('frontend/src/app/page.tsx', "<img ", "<Image width={800} height={600} ")
replace_in_file('frontend/src/app/page.tsx', "src=\"/dashboard-mockup.png\"", "src=\"/dashboard-mockup.png\" alt=\"Dashboard Mockup\"")
replace_in_file('frontend/src/app/page.tsx', "import Link from 'next/link';", "import Link from 'next/link';\nimport Image from 'next/image';")


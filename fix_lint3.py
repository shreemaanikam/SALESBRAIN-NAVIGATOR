import re

def replace_in_file(path, old, new):
    with open(path, 'r') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)

replace_in_file('frontend/src/app/dashboard/customers/page.tsx', "(segment as any).name", "(segment as { name?: string }).name")
replace_in_file('frontend/src/app/dashboard/data/page.tsx', "Database,   Activity", "Database")
replace_in_file('frontend/src/app/dashboard/page.tsx', "mockKpis as any", "mockKpis as unknown as Metric[]")
replace_in_file('frontend/src/app/dashboard/page.tsx', "mockSalesTrend as any", "mockSalesTrend as unknown as ChartData[]")
replace_in_file('frontend/src/app/dashboard/page.tsx', "mockCategorySales as any", "mockCategorySales as unknown as ChartData[]")
replace_in_file('frontend/src/app/dashboard/page.tsx', "mockInsights as any", "mockInsights as unknown as Insight[]")
replace_in_file('frontend/src/app/dashboard/risk/page.tsx', "const { data: outlierData, loading } = useApiData(getOutliers", "const { data: outlierData } = useApiData(getOutliers")
replace_in_file('frontend/src/app/dashboard/what-if/page.tsx', "useState<any>(null)", "useState<unknown>(null)")

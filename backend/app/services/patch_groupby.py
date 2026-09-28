import re

def patch_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Sales Trend
    content = content.replace(
        'trend = dft.groupby("_period")[col("sales")].sum().reset_index()',
        'trend = dft.groupby("_period").agg(sales=(col("sales"), "sum")).reset_index()'
    )
    content = content.replace(
        'profit_trend = dft2.groupby("_period")[profit_col].sum().reset_index()',
        'profit_trend = dft2.groupby("_period").agg(profit=(profit_col, "sum")).reset_index()'
    )
    content = content.replace(
        'trend = trend.merge(profit_trend[["_period", profit_col]], on="_period", how="left")',
        'trend = trend.merge(profit_trend[["_period", "profit"]], on="_period", how="left")'
    )
    content = content.replace(
        'trend = trend.rename(columns={col("sales"): "sales", profit_col: "profit", "_period": "period"})',
        'trend = trend.rename(columns={"_period": "period"})'
    )
    content = content.replace(
        'trend = trend.rename(columns={col("sales"): "sales", "_period": "period"})',
        'trend = trend.rename(columns={"_period": "period"})'
    )

    # 2. Category Breakdown
    content = content.replace(
        'cat_df = df.groupby(cat_col)[col("sales")].sum().reset_index()\n        cat_df.columns = ["name", "value"]',
        'cat_df = df.groupby(cat_col).agg(value=(col("sales"), "sum")).reset_index()\n        cat_df = cat_df.rename(columns={cat_col: "name"})'
    )
    content = content.replace(
        'p = df.groupby(cat_col)[col("profit")].sum().reset_index()\n            p.columns = ["name", "profit"]',
        'p = df.groupby(cat_col).agg(profit=(col("profit"), "sum")).reset_index()\n            p = p.rename(columns={cat_col: "name"})'
    )

    # 3. Product Performance
    content = content.replace(
        'prod_df = df.groupby(prod_col)[col("sales")].sum().reset_index()\n        prod_df.columns = ["name", "sales"]',
        'prod_df = df.groupby(prod_col).agg(sales=(col("sales"), "sum")).reset_index()\n        prod_df = prod_df.rename(columns={prod_col: "name"})'
    )
    content = content.replace(
        'pp = df.groupby(prod_col)[col("profit")].sum().reset_index()\n            pp.columns = ["name", "profit"]',
        'pp = df.groupby(prod_col).agg(profit=(col("profit"), "sum")).reset_index()\n            pp = pp.rename(columns={prod_col: "name"})'
    )

    # 4. Geographic Summary
    content = content.replace(
        'geo_df = df.groupby(geo_col)[col("sales")].sum().reset_index()\n        geo_df.columns = ["name", "sales"]',
        'geo_df = df.groupby(geo_col).agg(sales=(col("sales"), "sum")).reset_index()\n        geo_df = geo_df.rename(columns={geo_col: "name"})'
    )
    content = content.replace(
        'gp = df.groupby(geo_col)[col("profit")].sum().reset_index()\n            gp.columns = ["name", "profit"]',
        'gp = df.groupby(geo_col).agg(profit=(col("profit"), "sum")).reset_index()\n            gp = gp.rename(columns={geo_col: "name"})'
    )

    # 5. Segment Analysis
    content = content.replace(
        'seg_df = df.groupby(col("segment"))[col("sales")].sum().reset_index()\n        seg_df.columns = ["name", "sales"]',
        'seg_df = df.groupby(col("segment")).agg(sales=(col("sales"), "sum")).reset_index()\n        seg_df = seg_df.rename(columns={col("segment"): "name"})'
    )
    content = content.replace(
        'sp = df.groupby(col("segment"))[col("profit")].sum().reset_index()\n            sp.columns = ["name", "profit"]',
        'sp = df.groupby(col("segment")).agg(profit=(col("profit"), "sum")).reset_index()\n            sp = sp.rename(columns={col("segment"): "name"})'
    )

    with open(filepath, "w") as f:
        f.write(content)

patch_file("backend/app/services/workspace_service.py")

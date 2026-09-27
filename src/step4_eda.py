# ==========================================
# SalesBrain Navigator
# Step 4 - Exploratory Data Analysis (EDA)
# ==========================================

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

import pandas as pd
import seaborn as sns
import os

# ------------------------------------------------
# Create Images Folder Automatically
# ------------------------------------------------

os.makedirs("images", exist_ok=True)

# ------------------------------------------------
# Load Clean Dataset
# ------------------------------------------------

df = pd.read_csv("dataset/Cleaned_SuperStore.csv")
import numpy as np

# ----------------------------
# Clean Numeric Data
# ----------------------------

df.replace([np.inf, -np.inf], np.nan, inplace=True)

# ----------------------------
# Convert Dates
# ----------------------------

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

# ----------------------------
# Shipping Days
# ----------------------------

df["Shipping_Days"] = (
    df["ship_date"] -
    df["order_date"]
).dt.days

df["Shipping_Days"] = df["Shipping_Days"].clip(lower=0)

# ----------------------------
# Profit Margin
# ----------------------------

df["Profit_Margin"] = np.where(
    df["sales"] != 0,
    (df["profit"] / df["sales"]) * 100,
    np.nan
)

df.replace([np.inf, -np.inf], np.nan, inplace=True)

print("="*60)
print("SalesBrain Navigator - Exploratory Data Analysis")
print("="*60)

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10,6)

print(df.columns.tolist())

# ------------------------------------------------
# Chart 1
# Monthly Sales Trend
# ------------------------------------------------

monthly_sales = df.groupby("Month_Name")["sales"].sum()

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

monthly_sales = monthly_sales.reindex(month_order)

plt.figure(figsize=(12,6))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker='o',
    linewidth=3,
    markersize=8,
    color="#1565C0"
)

plt.title(
    "Monthly Sales Trend",
    fontsize=20,
    fontweight="bold"
)

plt.xlabel("Month", fontsize=14)
plt.ylabel("Total Sales", fontsize=14)

plt.grid(True, linestyle="--", alpha=0.4)

plt.xticks(rotation=45)

# Add value labels
for i, value in enumerate(monthly_sales.values):
    plt.text(
        i,
        value + 15000,
        f"{value/1000000:.2f}M",
        ha="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    "images/chart1_monthly_sales.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------
# Chart 2 - Sales by Category
# ------------------------------------------------

category_sales = (
    df.groupby("category")["sales"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

bars = plt.bar(
    category_sales.index,
    category_sales.values,
    color=["#1565C0", "#43A047", "#FB8C00"]
)

plt.title("Sales by Category", fontsize=18, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Total Sales")

# Add value labels
for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        value,
        f"{value/1000000:.2f}M",
        ha="center",
        va="bottom",
        fontsize=10
    )

plt.tight_layout()

plt.savefig(
    "images/chart2_sales_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Technology and Furniture contribute the highest revenue.")


# ------------------------------------------------
# Chart 3 - Profit by Category
# ------------------------------------------------

category_profit = (
    df.groupby("category")["profit"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

bars = plt.bar(
    category_profit.index,
    category_profit.values,
    color=["#2E7D32", "#1E88E5", "#F57C00"]
)

plt.title("Profit by Category", fontsize=18, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Total Profit")

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        value,
        f"{value/1000:.0f}K",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

plt.savefig(
    "images/chart3_profit_by_category.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Technology contributes the highest overall profit.")


# ------------------------------------------------
# Chart 4 - Sales by Region
# ------------------------------------------------

region_sales = (
    df.groupby("region")["sales"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

bars = plt.bar(region_sales.index, region_sales.values)

plt.xticks(rotation=45)

plt.title("Sales by Region", fontsize=18, fontweight="bold")
plt.xlabel("Region")
plt.ylabel("Total Sales")

plt.tight_layout()

plt.savefig(
    "images/chart4_sales_by_region.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("The top-performing regions contribute significantly more revenue than the lower-performing regions.")


# ------------------------------------------------
# Chart 5 - Profit by Region
# ------------------------------------------------

region_profit = (
    df.groupby("region")["profit"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(12,6))

bars = plt.bar(
    region_profit.index,
    region_profit.values,
    color="#43A047"
)

plt.title("Profit by Region", fontsize=18, fontweight="bold")
plt.xlabel("Region")
plt.ylabel("Total Profit")

plt.xticks(rotation=45)

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        value,
        f"{value/1000:.0f}K",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    "images/chart5_profit_by_region.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Identify which region generates the highest profit and which regions need improvement.")


# ------------------------------------------------
# Chart 6 - Sales by Market
# ------------------------------------------------

market_sales = (
    df.groupby("market")["sales"]
      .sum()
      .sort_values(ascending=False)
)

plt.figure(figsize=(10,6))

bars = plt.bar(
    market_sales.index,
    market_sales.values,
    color="#1565C0"
)

plt.title("Sales by Market", fontsize=18, fontweight="bold")
plt.xlabel("Market")
plt.ylabel("Total Sales")

plt.xticks(rotation=30)

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2,
        value,
        f"{value/1000000:.2f}M",
        ha="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    "images/chart6_sales_by_market.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Markets with the highest sales should receive greater business focus.")


# ------------------------------------------------
# Chart 7 - Customer Segment
# ------------------------------------------------

segment_sales = (
    df.groupby("segment")["sales"]
      .sum()
)

plt.figure(figsize=(8,8))

plt.pie(
    segment_sales,
    labels=segment_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Customer Segment Distribution",
    fontsize=18,
    fontweight="bold"
)

plt.savefig(
    "images/chart7_customer_segment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("The Consumer segment generally contributes the largest share of sales.")


# ------------------------------------------------
# Chart 8 - Order Priority
# ------------------------------------------------

priority = (
    df["order_priority"]
      .value_counts()
)

plt.figure(figsize=(8,8))

plt.pie(
    priority,
    labels=priority.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Order Priority Distribution",
    fontsize=18,
    fontweight="bold"
)

plt.savefig(
    "images/chart8_order_priority.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most customer orders fall under Medium and High priority.")


# ------------------------------------------------
# Chart 9 - Top 10 Products by Sales
# ------------------------------------------------

top_products = (
    df.groupby("product_name")["sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,7))

bars = plt.barh(
    top_products.index,
    top_products.values,
    color="#1565C0"
)

plt.title("Top 10 Products by Sales", fontsize=18, fontweight="bold")
plt.xlabel("Total Sales")
plt.ylabel("Product")

for bar in bars:
    value = bar.get_width()
    plt.text(
        value,
        bar.get_y()+bar.get_height()/2,
        f"{value/1000:.0f}K",
        va="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    "images/chart9_top_products.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Top-selling products contribute a significant portion of total revenue.")


# ------------------------------------------------
# Chart 10 - Top 10 Countries
# ------------------------------------------------

top_countries = (
    df.groupby("country")["sales"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
)

plt.figure(figsize=(12,6))

bars = plt.bar(
    top_countries.index,
    top_countries.values,
    color="#43A047"
)

plt.title("Top 10 Countries by Sales", fontsize=18, fontweight="bold")
plt.xlabel("Country")
plt.ylabel("Total Sales")

plt.xticks(rotation=45)

for bar in bars:
    value = bar.get_height()
    plt.text(
        bar.get_x()+bar.get_width()/2,
        value,
        f"{value/1000000:.2f}M",
        ha="center",
        fontsize=9
    )

plt.tight_layout()

plt.savefig(
    "images/chart10_top_countries.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("The top-performing countries generate the largest share of global sales.")


# ------------------------------------------------
# Chart 11 - Sales Distribution
# ------------------------------------------------

plt.figure(figsize=(10,6))

plt.hist(
    df["sales"],
    bins=30,
    color="#1565C0",
    edgecolor="black"
)

plt.title("Sales Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/chart11_sales_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most sales transactions are small, while a few high-value orders contribute significantly.")


# ------------------------------------------------
# Chart 12 - Profit Distribution
# ------------------------------------------------

plt.figure(figsize=(10,6))

plt.hist(
    df["profit"],
    bins=30,
    color="#FB8C00",
    edgecolor="black"
)

plt.title("Profit Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Profit")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/chart12_profit_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most orders generate moderate profit, while a few produce exceptionally high profits or losses.")


# ------------------------------------------------
# Chart 13 - Sales vs Profit
# ------------------------------------------------

plt.figure(figsize=(10,6))

plt.scatter(
    df["sales"],
    df["profit"],
    alpha=0.4,
    color="royalblue"
)

plt.title("Sales vs Profit", fontsize=18, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Profit")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "images/chart13_sales_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Higher sales generally lead to higher profit, although some high-sales orders still generate losses.")


# ------------------------------------------------
# Chart 14 - Discount vs Profit
# ------------------------------------------------

plt.figure(figsize=(10,6))

plt.scatter(
    df["discount"],
    df["profit"],
    alpha=0.4,
    color="tomato"
)

plt.title("Discount vs Profit", fontsize=18, fontweight="bold")
plt.xlabel("Discount")
plt.ylabel("Profit")

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "images/chart14_discount_profit.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Large discounts often reduce profitability.")


import seaborn as sns

# ------------------------------------------------
# Chart 15 - Correlation Heatmap
# ------------------------------------------------

numeric = df.select_dtypes(include=["number"])

plt.figure(figsize=(8,6))

sns.heatmap(
    numeric.corr(),
    annot=True,
    cmap="Blues",
    fmt=".2f"
)

plt.title("Correlation Heatmap", fontsize=18, fontweight="bold")

plt.tight_layout()

plt.savefig(
    "images/chart15_correlation_heatmap.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("The heatmap highlights relationships among numerical business variables.")


# ------------------------------------------------
# Chart 16 - Sales Boxplot
# ------------------------------------------------

plt.figure(figsize=(8,6))

plt.boxplot(df["sales"])

plt.title("Sales Boxplot", fontsize=18, fontweight="bold")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "images/chart16_sales_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Sales contain several high-value outliers.")


# ------------------------------------------------
# Chart 17 - Profit Boxplot
# ------------------------------------------------

plt.figure(figsize=(8,6))

plt.boxplot(df["profit"])

plt.title("Profit Boxplot", fontsize=18, fontweight="bold")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(
    "images/chart17_profit_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Profit contains both positive and negative outliers.")


# ------------------------------------------------
# Chart 18 - Shipping Days Distribution
# ------------------------------------------------

shipping_days = df["Shipping_Days"].dropna()

plt.figure(figsize=(10,6))

plt.hist(
    shipping_days,
    bins=20,
    color="green",
    edgecolor="black"
)

plt.title("Shipping Days Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Shipping Days")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/chart18_shipping_days.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most orders are delivered within a common shipping duration.")



# ------------------------------------------------
# Chart 19 - Profit Margin Distribution
# ------------------------------------------------

profit_margin = df["Profit_Margin"].dropna()

plt.figure(figsize=(10,6))

plt.hist(
    profit_margin,
    bins=30,
    color="purple",
    edgecolor="black"
)

plt.title("Profit Margin Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "images/chart19_profit_margin.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most products have moderate profit margins while only a few have exceptionally high or low margins.")


# ------------------------------------------------
# Chart 20 - Sales Density Plot (KDE)
# ------------------------------------------------

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,6))

sns.kdeplot(
    data=df,
    x="sales",
    fill=True,
    color="royalblue",
    linewidth=2
)

plt.title("Sales Density Distribution", fontsize=18, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Density")

plt.tight_layout()

plt.savefig(
    "images/chart20_sales_kde.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Most sales occur in lower value ranges, while high-value sales are relatively rare.")


# ------------------------------------------------
# Chart 21 - Sales by Category (Violin Plot)
# ------------------------------------------------

plt.figure(figsize=(10,6))

sns.violinplot(
    data=df,
    x="category",
    y="sales",
    hue="category",
    palette="Set2",
    legend=False
)

plt.title("Sales Distribution by Category", fontsize=18, fontweight="bold")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    "images/chart21_sales_violin.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Technology products generally have higher-value sales and a wider sales distribution.")


# ------------------------------------------------
# Chart 22 - Pair Plot
# ------------------------------------------------

pair_columns=[
    "sales",
    "profit",
    "quantity",
    "discount"
]
sns.pairplot(
    df[pair_columns],
    diag_kind="kde",
    corner=True
)

plt.savefig(
    "images/chart22_pairplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("The pair plot reveals relationships among Sales, Profit, Quantity, and Discount simultaneously.")


# ------------------------------------------------
# Chart 23 - Bubble Chart
# ------------------------------------------------

plt.figure(figsize=(10,7))

plt.scatter(
    df["sales"],
    df["profit"],
    s=df["quantity"]*8,
    alpha=0.45,
    color="dodgerblue",
    edgecolors="black"
)

plt.title("Sales vs Profit (Bubble Size = Quantity)", fontsize=18, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(
    "images/chart23_bubble_chart.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print("Larger orders generally generate higher profit, although some large orders still result in losses.")


# ------------------------------------------------
# Chart 24 - Sales Outliers (IQR Method)
# ------------------------------------------------

Q1 = df["sales"].quantile(0.25)
Q3 = df["sales"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

normal = df[
    (df["sales"] >= lower) &
    (df["sales"] <= upper)
]

outliers = df[
    (df["sales"] < lower) |
    (df["sales"] > upper)
]

plt.figure(figsize=(10,6))

plt.scatter(
    normal["sales"],
    normal["profit"],
    color="steelblue",
    alpha=0.4,
    label="Normal"
)

plt.scatter(
    outliers["sales"],
    outliers["profit"],
    color="red",
    alpha=0.8,
    label="Outliers"
)

plt.title("Sales Outliers using IQR Method", fontsize=18, fontweight="bold")
plt.xlabel("Sales")
plt.ylabel("Profit")
plt.legend()

plt.tight_layout()

plt.savefig(
    "images/chart24_outliers_iqr.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print(f"Detected {len(outliers)} sales outliers using the IQR method. These high-value transactions may require separate business analysis.")


# ------------------------------------------------
# Chart 25 - Outlier Summary Table
# ------------------------------------------------

Q1 = df["sales"].quantile(0.25)
Q3 = df["sales"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["sales"] < lower) |
    (df["sales"] > upper)
]

print("=" * 50)
print("OUTLIER SUMMARY")
print("=" * 50)

print(f"Lower Fence : {lower:.2f}")
print(f"Upper Fence : {upper:.2f}")
print(f"Total Outliers : {len(outliers)}")

print("\nTop 10 Highest Sales Outliers\n")

print(
    outliers[
        [
            "sales",
            "profit",
            "category",
            "region",
            "product_name"
        ]
    ]
    .sort_values(by="sales", ascending=False)
    .head(10)
)

outliers[
    [
        "sales",
        "profit",
        "category",
        "region",
        "product_name"
    ]
].sort_values(
    by="sales",
    ascending=False
).to_csv(
    "images/outlier_summary.csv",
    index=False
)

print("\n✅ Outlier Summary saved to images/outlier_summary.csv")


# ------------------------------------------------
# Chart 25 - (Outlier Count Chart)
# ------------------------------------------------

Q1 = df["sales"].quantile(0.25)
Q3 = df["sales"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

outliers = df[
    (df["sales"] < lower) |
    (df["sales"] > upper)
]

normal = len(df) - len(outliers)

plt.figure(figsize=(7,5))

plt.bar(
    ["Normal Data", "Outliers"],
    [normal, len(outliers)]
)

plt.title("Outlier Detection using IQR", fontsize=16, fontweight="bold")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    "images/chart25_outlier_count.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nBusiness Insight:")
print(f"{len(outliers)} records ({len(outliers)/len(df)*100:.2f}%) are identified as sales outliers using the IQR method.")




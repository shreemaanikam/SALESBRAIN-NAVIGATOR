# ==========================================
# SalesBrain Navigator
# Step 3 - Data Cleaning & Preprocessing
# ==========================================

import pandas as pd

print("=" * 60)
print("SalesBrain Navigator - Data Cleaning")
print("=" * 60)

# Load dataset
df = pd.read_csv("dataset/SuperStoreOrders.csv", encoding="latin1")

# --------------------------------------------------
# 1. Rename first column (Remove BOM character)
# --------------------------------------------------

df.rename(columns={"ï»¿order_id": "order_id"}, inplace=True)

# --------------------------------------------------
# 2. Convert Dates
# --------------------------------------------------

# cspell:ignore dayfirst
# Convert mixed date formats
# Convert mixed date formats safely
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="mixed",
    dayfirst=False,
    errors="coerce"
)

df["ship_date"] = pd.to_datetime(
    df["ship_date"],
    format="mixed",
    dayfirst=False,
    errors="coerce"
)

# --------------------------------------------------
# 3. Convert Sales to Numeric
# --------------------------------------------------

df["sales"] = (
    df["sales"]
    .replace(r"[\$,]", "", regex=True)
    .astype(float)
)

# --------------------------------------------------
# 4. Check Missing Values
# --------------------------------------------------

print("\nMissing Values\n")
print(df.isnull().sum())

# --------------------------------------------------
# 5. Check Duplicate Rows
# --------------------------------------------------

print("\nDuplicate Records:", df.duplicated().sum())

# --------------------------------------------------
# 6. Remove Duplicates
# --------------------------------------------------

df.drop_duplicates(inplace=True)

# --------------------------------------------------
# 7. Dataset Shape After Cleaning
# --------------------------------------------------

print("\nDataset Shape After Cleaning")
print(df.shape)

# --------------------------------------------------
# 8. Check Data Types
# --------------------------------------------------

print("\nUpdated Data Types\n")
print(df.dtypes)

# --------------------------------------------------
# 9. Save Clean Dataset
# --------------------------------------------------

df.to_csv("dataset/Cleaned_SuperStore.csv", index=False)

print("\n✅ Clean Dataset Saved Successfully!")



# ==================================================
# Feature Engineering
# ==================================================

print("\n" + "="*60)
print("Feature Engineering")
print("="*60)

# Month Number
df["Month"] = df["order_date"].dt.month

# Month Name
df["Month_Name"] = df["order_date"].dt.month_name()

# Quarter
df["Quarter"] = df["order_date"].dt.quarter

# Day
df["Day"] = df["order_date"].dt.day

# Day Name
df["Day_Name"] = df["order_date"].dt.day_name()

# Shipping Days
df["Shipping_Days"] = (
    df["ship_date"] - df["order_date"]
).dt.days

# Profit Margin (%)
df["Profit_Margin"] = (
    df["profit"] / df["sales"]
) * 100

print("\nNew Features Created Successfully!\n")

print(df[[
    "order_date",
    "Month",
    "Month_Name",
    "Quarter",
    "Day_Name",
    "Shipping_Days",
    "Profit_Margin"
]].head())

# Save Updated Dataset
df.to_csv("dataset/Cleaned_SuperStore.csv", index=False)

print("\n✅ Feature Engineered Dataset Saved Successfully!")


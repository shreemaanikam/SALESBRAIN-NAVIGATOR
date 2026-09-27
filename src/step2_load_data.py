# ==========================================
# SalesBrain Navigator
# Step 2 - Load Dataset
# ==========================================

import pandas as pd

print("=" * 60)
print("SalesBrain Navigator - Dataset Loading")
print("=" * 60)

# Load the dataset
df = pd.read_csv(
    "dataset/SuperStoreOrders.csv",
    encoding="utf-8-sig"
)

print("\n Dataset Loaded Successfully!")

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nDataset Information")
df.info()

print("\nColumn Names")
print(df.columns)

print("\nStatistical Summary")
print(df.describe())


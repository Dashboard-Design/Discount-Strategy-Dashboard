import pandas as pd

df = pd.read_excel("dataset/sample_-_superstore.xls")

# Summarize by Category + Sub-Category
summary = (
    df.groupby(["Category", "Sub-Category"], as_index=False)
      .agg(Sales=("Sales", "sum"))
      .sort_values(["Category", "Sub-Category"])
)


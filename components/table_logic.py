import pandas as pd
import numpy as np
from components.Discount_logic import discount_strategy


def summary(df, filtered, year, region):
    filtered_data = filtered
    if filtered_data.empty:
        return pd.DataFrame()

    # --- Base aggregation ---
    sub = (
        filtered_data.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Discount=("Discount", "mean"),
            Quantity=("Quantity", "sum")
        )
    )

    # Keep numeric before formatting
    sub["Revenue_num"] = sub["Revenue"]
    sub["Profit_num"] = sub["Profit"]
    sub["Discount_num"] = sub["Discount"]


    # --- YoY Revenue ---
    prev_year = str(int(year) - 1)
    prev_f = df[df["Year"] == prev_year]
    if region != "All":
        prev_f = prev_f[prev_f["Region"] == region]

    prev = (
        prev_f.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(Revenue_prev=("Sales", "sum"))
    )
    sub = sub.merge(prev, on=["Category", "Sub-Category"], how="left")

    sub["YoY Revenue %"] = np.where(
        sub["Revenue_prev"] > 0,
        ((sub["Revenue"] - sub["Revenue_prev"]) / sub["Revenue_prev"]).round(3),
        None
    )
    sub.drop(columns=["Revenue_prev"], inplace=True)

    # --- Revenue Trend (numeric list for gt sparklines) ---
    trend_data = (
        df.groupby(["Category", "Sub-Category", "Year"], as_index=False)["Sales"].sum()
    )
    trend_data["Year"] = trend_data["Year"].astype(int)

    def build_trend(cat, subcat):
        series = trend_data[
            (trend_data["Category"] == cat) & (trend_data["Sub-Category"] == subcat)
        ].sort_values("Year")
        return series["Sales"].tolist()

    sub["Revenue Trend (All Years)"] = sub.apply(
        lambda r: build_trend(r["Category"], r["Sub-Category"]), axis=1
    )

    # --- Rank ---
    sub["Rank"] = sub.groupby("Category")["Revenue"].rank(method="dense", ascending=False).astype(int)

    # --- Discount Strategy ---
    sub["Discount Strategy"] = sub.apply(discount_strategy, axis=1)

    # --- Category Icons ---
    icon_map = {
        "Furniture": "<img src='https://img.icons8.com/fluency/20/000000/armchair.png' style='vertical-align:middle;margin-right:6px;'/> Furniture",
        "Office Supplies": "<img src='https://img.icons8.com/fluency/20/000000/box.png' style='vertical-align:middle;margin-right:6px;'/> Office Supplies",
        "Technology": "<img src='https://img.icons8.com/fluency/20/000000/laptop.png' style='vertical-align:middle;margin-right:6px;'/> Technology"
    }

    rows = []
    cats = list(sub["Category"].unique())
    for cat in cats:
        cat_df = sub[sub["Category"] == cat].copy()
        cat_df["Category_Display"] = np.nan
        if len(cat_df) > 0:
            cat_df.iloc[0, cat_df.columns.get_loc("Category_Display")] = icon_map.get(cat, cat)

        display_cols = [
            "Category_Display", "Sub-Category", "Rank", "Revenue", "Quantity", "Profit",
            "YoY Revenue %", "Discount", "Discount Strategy", "Revenue Trend (All Years)"
        ]
        rows.append(cat_df[display_cols])

        # Totals row
        total_row = {
            "Category_Display": "Total",
            "Sub-Category": np.nan,
            "Rank": np.nan,
            "Revenue": cat_df["Revenue"].sum(),
            "Quantity": cat_df["Quantity"].sum(),
            "Profit": cat_df["Profit"].sum(),
            "YoY Revenue %": np.nan,
            "Discount": cat_df["Discount"].mean(),
            "Discount Strategy": np.nan,
            "Revenue Trend (All Years)": [np.nan]
        }
        empty_row = {col: np.nan for col in display_cols}
        rows.append(pd.DataFrame([total_row], columns=display_cols))
        rows.append(pd.DataFrame([empty_row], columns=display_cols))

    final_df = pd.concat(rows, ignore_index=True)
    return final_df

# table_logic.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from components.Discount_logic import discount_strategy


def make_sparkline(values, color="#1f77b4"):
    """Generate base64-encoded sparkline from list of values."""
    fig, ax = plt.subplots(figsize=(2, 0.4))  # small sparkline
    ax.plot(values, color=color, linewidth=1.5)
    ax.fill_between(range(len(values)), values, min(values), color=color, alpha=0.15)
    ax.axis("off")
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    return f"<img src='data:image/png;base64,{base64.b64encode(buf.read()).decode()}'/>"


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
        ((sub["Revenue_num"] - sub["Revenue_prev"]) / sub["Revenue_prev"] * 100).round(1),
        None
    )
    sub.drop(columns=["Revenue_prev"], inplace=True)

    # --- Revenue Trend (sparklines) ---
    trend_data = (
        df.groupby(["Category", "Sub-Category", "Year"], as_index=False)["Sales"].sum()
    )
    trend_data["Year"] = trend_data["Year"].astype(int)

    def build_trend(cat, subcat):
        series = trend_data[
            (trend_data["Category"] == cat) & (trend_data["Sub-Category"] == subcat)
        ].sort_values("Year")
        return make_sparkline(series["Sales"].tolist())

    sub["Revenue Trend (All Years)"] = sub.apply(
        lambda r: build_trend(r["Category"], r["Sub-Category"]), axis=1
    )

    # --- Rank ---
    sub["Rank"] = sub.groupby("Category")["Revenue_num"].rank(method="dense", ascending=False).astype(int)

    # --- Discount Strategy ---
    sub["Discount Strategy"] = sub.apply(discount_strategy, axis=1)

    # --- Inline Formatting ---
    sub["Revenue"] = sub["Revenue_num"].apply(lambda x: f"${x/1000:.1f}K" if pd.notna(x) else "")
    sub["Profit"] = sub["Profit_num"].apply(lambda x: f"${x/1000:.1f}K" if pd.notna(x) else "")
    sub["Quantity"] = sub["Quantity"].apply(lambda x: f"{int(x)}" if pd.notna(x) else "")
    sub["YoY Revenue %"] = sub["YoY Revenue %"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "")
    sub["Discount %"] = (sub["Discount_num"] * 100).apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "")

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
        icon_html = icon_map.get(cat, cat)
        cat_df["Category_Display"] = ""
        if len(cat_df) > 0:
            cat_df.iloc[0, cat_df.columns.get_loc("Category_Display")] = icon_html

        display_cols = [
            "Category_Display", "Sub-Category", "Rank", "Revenue", "Quantity", "Profit",
            "YoY Revenue %", "Discount %", "Revenue Trend (All Years)", "Discount Strategy"
        ]
        rows.append(cat_df[display_cols])

        # Totals (numeric only)
        tot_rev = cat_df["Revenue_num"].sum()
        tot_profit = cat_df["Profit_num"].sum()
        tot_qty = cat_df["Quantity"].astype(int).sum()
        tot_disc = cat_df["Discount_num"].mean()

        total_row = {
            "Category_Display": "Total",
            "Sub-Category": "",
            "Rank": "",
            "Revenue": f"${tot_rev/1000:.1f}K",
            "Quantity": f"{tot_qty}",
            "Profit": f"${tot_profit/1000:.1f}K",
            "YoY Revenue %": "",
            "Discount %": f"{tot_disc*100:.1f}%" if pd.notna(tot_disc) else "",
            "Revenue Trend (All Years)": "",
            "Discount Strategy": ""
        }
        empty_row = {col: " " for col in display_cols}
        rows.append(pd.DataFrame([total_row], columns=display_cols))
        rows.append(pd.DataFrame([empty_row], columns=display_cols))

    final_df = pd.concat(rows, ignore_index=True)
    return final_df

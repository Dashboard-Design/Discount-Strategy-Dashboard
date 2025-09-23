import pandas as pd
import numpy as np
import base64
from components.Discount_logic import discount_strategy

def summary(df, filtered, year, region,  company_goal, customer_priority ):
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
        df.groupby(["Category", "Sub-Category", "Year"], as_index=False).agg(
            Revenue=("Sales", "sum"),
            Discount=("Discount", "mean")
        )
    )
    trend_data["Year"] = trend_data["Year"].astype(int)

    def build_trend(cat, subcat):
        series = trend_data[
            (trend_data["Category"] == cat) & (trend_data["Sub-Category"] == subcat)
        ].sort_values("Year")
        
        # Convert the revenue values to a space-separated string
        trend_values = series["Revenue"].tolist()
        
        # Handle empty or None values
        if not trend_values or all(pd.isna(v) for v in trend_values):
            return ""
        
        # Filter out NaN values and convert to string
        valid_values = [str(v) for v in trend_values if not pd.isna(v)]
        
        # Return as space-separated string
        return " ".join(valid_values)

    sub["Revenue Trend (All Years)"] = sub.apply(
        lambda r: build_trend(r["Category"], r["Sub-Category"]), axis=1
    )

    # --- Elasticity Proxy (Discount vs Revenue correlation) ---
    def calc_elasticity(cat, subcat):
        series = trend_data[
            (trend_data["Category"] == cat) & (trend_data["Sub-Category"] == subcat)
        ]
        if len(series) >= 3:  # need at least 3 years to measure correlation
            corr = series["Discount"].corr(series["Revenue"])
            return round(corr, 2) if pd.notna(corr) else 0
        return 0

    sub["Elasticity Proxy"] = sub.apply(
        lambda r: calc_elasticity(r["Category"], r["Sub-Category"]), axis=1
    )

    def format_elasticity(value):
        if value > 0.5:
            return f'<span class="elasticity-positive">●</span> {value}'
        elif value < -0.5:
            return f'<span class="elasticity-negative">●</span> {value}'
        else:
            return f'<span class="elasticity-neutral">●</span> {value}'

    sub["Elasticity Proxy"] = sub.apply(
        lambda r: format_elasticity(r["Elasticity Proxy"]), axis=1
    )

    # --- Rank ---
    sub["Rank"] = sub.groupby("Category")["Revenue"].rank(method="dense", ascending=False).astype(int)

    # --- Discount Strategy ---
    sub["Discount Strategy"] = sub.apply(
        lambda row: discount_strategy(row, company_goal, customer_priority),
        axis=1
    )

    # --- Category Icons ---
    def img_to_base64(path):
        with open(path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")
        return f"data:image/png;base64,{encoded}"

    icon_map = {
    "Furniture": f"<img src='{img_to_base64('images/icons8_wing_chair_1.png')}' style='width:26px;height:26px;vertical-align:middle;margin-right:4px;'/> Furniture",
    "Office Supplies": f"<img src='{img_to_base64('images/icons8_print _1.png')}' style='width:26px;height:26px;vertical-align:middle;margin-right:4px;'/> Office Supplies",
    "Technology": f"<img src='{img_to_base64('images/icons8_server_1.png')}' style='width:24px;height:24px;vertical-align:middle;margin-right:4px;'/> Technology"
    }


    sub = sub.sort_values(by=["Category", "Rank"], ascending= True)
    rows = []
    cats = list(sub["Category"].unique())
    for cat in cats:
        cat_df = sub[sub["Category"] == cat].copy()
        cat_df["Category_Display"] = ""
        if len(cat_df) > 0:
            cat_df.iloc[0, cat_df.columns.get_loc("Category_Display")] = icon_map.get(cat, cat)

        display_cols = [
            "Category_Display", "Sub-Category", "Rank", "Revenue", "Quantity", "Profit",
            "YoY Revenue %", "Revenue Trend (All Years)", "Discount", "Elasticity Proxy", "Discount Strategy"
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
            "Revenue Trend (All Years)": " ",
            "Discount": cat_df["Discount"].mean(),
            "Elasticity Proxy": np.nan,
            "Discount Strategy": np.nan,
        }
        # empty_row = {col: np.nan for col in display_cols}
        rows.append(pd.DataFrame([total_row], columns=display_cols))
        # rows.append(pd.DataFrame([empty_row], columns=display_cols))

    final_df = pd.concat(rows, ignore_index=True)

    final_df["Category_Display"] = final_df["Category_Display"].astype(str)

    return final_df

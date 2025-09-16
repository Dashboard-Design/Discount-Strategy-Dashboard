import pandas as pd
import numpy as np

def summary(df, filtered, year, region):
    filtered_data = filtered
    if filtered_data.empty:
        return pd.DataFrame()

    # --- Base aggregation at Sub-Category level ---
    sub = (
        filtered_data.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(
            Revenue=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Discount=("Discount", "mean"),
            Orders=("Order ID", "nunique"),
            Quantity=("Quantity", "sum")
        )
    )

    # YoY Growth for Revenue: compare to previous year
    prev_year = str(int(year) - 1)
    if prev_year in df["Year"].unique():
        prev_f = df[df["Year"] == prev_year]
        if region != "All":
            prev_f = prev_f[prev_f["Region"] == region]

        prev = (
            prev_f.groupby(["Category", "Sub-Category"], as_index=False)
            .agg(Revenue_prev=("Sales", "sum"), Profit_prev=("Profit", "sum"))
        )
        sub = sub.merge(prev, on=["Category", "Sub-Category"], how="left")
        
        # YoY Revenue %
        sub["YoY Revenue %"] = np.where(
            sub["Revenue_prev"] > 0,
            ((sub["Revenue"] - sub["Revenue_prev"]) / sub["Revenue_prev"] * 100).round(1),
            None
        )
        
        # YoY Profit %  
        sub["YoY Profit %"] = np.where(
            sub["Profit_prev"] > 0,
            ((sub["Profit"] - sub["Profit_prev"]) / sub["Profit_prev"] * 100).round(1),
            None
        )
        
        sub.drop(columns=["Revenue_prev", "Profit_prev"], inplace=True)
    else:
        sub["YoY Revenue %"] = None
        sub["YoY Profit %"] = None

    # Rank by Revenue within each category
    sub["Rank"] = sub.groupby("Category")["Revenue"].rank(method="dense", ascending=False).astype(int)

    # Format values inline
    sub["Revenue"] = sub["Revenue"].apply(lambda x: f"${x/1000:.1f}K" if pd.notna(x) else "")
    sub["Profit"] = sub["Profit"].apply(lambda x: f"${x/1000:.1f}K" if pd.notna(x) else "")
    sub["YoY Revenue %"] = sub["YoY Revenue %"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "")
    sub["YoY Profit %"] = sub["YoY Profit %"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "")
    sub["Discount %"] = (sub["Discount"] * 100).apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "")

    # --- Build ordered rows with totals immediately after each category ---
    rows = []
    # Icon map
    icon_map = {
        "Furniture": "<img src='https://img.icons8.com/fluency/20/000000/armchair.png' style='vertical-align:middle;margin-right:6px;'/> Furniture",
        "Office Supplies": "<img src='https://img.icons8.com/fluency/20/000000/box.png' style='vertical-align:middle;margin-right:6px;'/> Office Supplies",
        "Technology": "<img src='https://img.icons8.com/fluency/20/000000/laptop.png' style='vertical-align:middle;margin-right:6px;'/> Technology"
    }

    # Get original numeric values before formatting for totals calculation
    sub_numeric = (
        filtered_data.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(
            Revenue_num=("Sales", "sum"),
            Profit_num=("Profit", "sum"),
            Discount_num=("Discount", "mean")
        )
    )

    # Iterate categories in a stable order
    cats = list(sub["Category"].unique())
    for cat in cats:
        cat_df = sub[sub["Category"] == cat].copy()
        cat_numeric = sub_numeric[sub_numeric["Category"] == cat].copy()
        
        # Sort by original revenue values (need to extract from numeric data)
        cat_numeric = cat_numeric.sort_values("Revenue_num", ascending=False)
        cat_df = cat_df.set_index(["Category", "Sub-Category"]).loc[
            cat_numeric.set_index(["Category", "Sub-Category"]).index
        ].reset_index()

        # Prepare Category_Display: icon + label only on first row
        icon_html = icon_map.get(cat, f"{cat}")
        cat_df["Category_Display"] = ""
        if len(cat_df) > 0:
            cat_df.iloc[0, cat_df.columns.get_loc("Category_Display")] = icon_html

        # Select only the required columns in the specified order
        display_cols = [
            "Category_Display", "Sub-Category", "Rank", "Revenue", "Profit", 
            "YoY Revenue %", "YoY Profit %", "Discount %"
        ]
        rows.append(cat_df[display_cols])

        # Build totals row using original numeric values
        tot_revenue = cat_numeric["Revenue_num"].sum()
        tot_profit = cat_numeric["Profit_num"].sum()
        tot_discount = cat_numeric["Discount_num"].mean()

        total_row = {
            "Category_Display": icon_html,
            "Sub-Category": "TOTAL",
            "Rank": "",
            "Revenue": f"${tot_revenue/1000:.1f}K",
            "Profit": f"${tot_profit/1000:.1f}K", 
            "YoY Revenue %": "",
            "YoY Profit %": "",
            "Discount %": f"{tot_discount*100:.1f}%" if pd.notna(tot_discount) else ""
        }
        rows.append(pd.DataFrame([total_row], columns=display_cols))

    # Concatenate rows in the right order
    final_df = pd.concat(rows, ignore_index=True)
    
    return final_df
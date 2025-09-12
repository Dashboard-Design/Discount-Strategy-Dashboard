import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Load data
df = pd.read_excel("dataset/sample_-_superstore.xls")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# --- Slicers ---
regions = st.multiselect(
    "Select Region(s)", 
    df["Region"].unique(), 
    default=df["Region"].unique()
)

date_range = st.date_input(
    "Select Date Range",
    [df["Order Date"].min().date(), df["Order Date"].max().date()]
)

# Filter data
mask = (
    df["Region"].isin(regions)
    & (df["Order Date"] >= pd.to_datetime(date_range[0]))
    & (df["Order Date"] <= pd.to_datetime(date_range[1]))
)
filtered_df = df.loc[mask]

# --- Build KPI table ---
kpis = []

kpis.append(pd.DataFrame({"KPI": ["Sales"], "Category": None, "Value": [filtered_df["Sales"].sum()]}))
kpis.append(pd.DataFrame({"KPI": ["Profit"], "Category": None, "Value": [filtered_df["Profit"].sum()]}))
kpis.append(pd.DataFrame({"KPI": ["Quantity"], "Category": None, "Value": [filtered_df["Quantity"].sum()]}))
kpis.append(pd.DataFrame({"KPI": ["Discount"], "Category": None, "Value": [filtered_df["Discount"].sum()]}))
kpis.append(pd.DataFrame({"KPI": ["Avg Profit per Order"], "Category": None, "Value": [filtered_df["Profit"].mean()]}))
kpis.append(pd.DataFrame({"KPI": ["Profit Margin"], "Category": None, "Value": [(filtered_df["Profit"].sum() / filtered_df["Sales"].sum()) * 100]}))

# Add breakdowns (by Category)
for cat in filtered_df["Category"].unique():
    kpis.append(pd.DataFrame({
        "KPI": ["Sales"], "Category": [cat], "Value": [filtered_df.loc[filtered_df["Category"] == cat, "Sales"].sum()]
    }))
    kpis.append(pd.DataFrame({
        "KPI": ["Profit"], "Category": [cat], "Value": [filtered_df.loc[filtered_df["Category"] == cat, "Profit"].sum()]
    }))
    kpis.append(pd.DataFrame({
        "KPI": ["Quantity"], "Category": [cat], "Value": [filtered_df.loc[filtered_df["Category"] == cat, "Quantity"].sum()]
    }))
    kpis.append(pd.DataFrame({
        "KPI": ["Discount"], "Category": [cat], "Value": [filtered_df.loc[filtered_df["Category"] == cat, "Discount"].sum()]
    }))

pivot_df = pd.concat(kpis, ignore_index=True)

# --- Configure AgGrid ---
gb = GridOptionsBuilder.from_dataframe(pivot_df)
gb.configure_default_column(groupable=True, editable=False)

# Group by KPI
gb.configure_column("KPI", rowGroup=True, hide=True)

# Show totals in Value column
gb.configure_column("Value", aggFunc="sum", type=["numericColumn", "numberColumnFilter", "customNumericFormat"])

grid_options = gb.build()

# --- Render Grid ---
st.subheader("KPI Breakdown Table")
AgGrid(
    pivot_df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    update_mode="MODEL_CHANGED",
    fit_columns_on_grid_load=True,
    width="100%",     # responsive full width
    height=600,       # make it bigger
    theme="alpine"    # clean look
)

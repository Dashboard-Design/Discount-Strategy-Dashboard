from great_tables import GT, style, loc
from shiny import ui
import polars as pl

def table_display(df_sum, year, region):
    if df_sum.empty:
        return ui.div(
            "No data available for the selected filters.",
            style="text-align: center; padding: 20px; font-size: 16px;"
        )

    # Convert Pandas 
    df_polars = pl.from_pandas(df_sum)

    region_display = region if region != "All" else "All Regions"

    tbl = (
        GT(df_polars)
        .tab_header(
            title=f"{region_display}, {year}",
            subtitle="Grouped by Category and Sub-Category"
        )
        .cols_label(
            **{
                "Category_Display": "Category",
                "Sub-Category": "Sub-Category",
                "Rank": "Rank",
                "Revenue": "Revenue",
                "Quantity": "Quantity",
                "Profit": "Profit",
                "YoY Revenue %": "YoY Revenue %",
                "Discount": "Discount %",
                "Discount Strategy": "Discount Strategy",
                "Revenue Trend (All Years)": "Revenue Trend"
            }
        )
        .cols_width(
            **{
                "Category_Display": "10%",
                "Sub-Category": "10%",
                "Rank": "9%",
                "Revenue": "9%",
                "Quantity": "9%",
                "Profit": "9%",
                "YoY Revenue %": "9%",
                "Discount": "9%",
                "Discount Strategy": "16%",
                "Revenue Trend (All Years)": "10%"
            }
        )
        # formatting ----
        .fmt_number(columns=["Revenue", "Profit"], compact=True, pattern="${x}", n_sigfig=3)
        .fmt_number(columns=["Quantity"], decimals=0)
        .fmt_number(columns=["Rank"], decimals=0)
        .fmt_percent(columns=["Discount"], decimals=1)
        .fmt_percent(columns=["YoY Revenue %"], decimals=1)
        
        # Trend sparkline 
        .fmt_nanoplot(
            "Revenue Trend (All Years)", 
            plot_type="line"
        )
        # Missing values
        .sub_missing(missing_text="")
        # Styles: Bold totals
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(rows=pl.col("Sub-Category") == "TOTAL")
        )
        .tab_style(
            style=style.text(weight="bold", color="black"),
            locations=loc.column_labels()
        )
        .tab_options(
            table_width="100%",
            container_width="100%",
            table_font_size="15px",
            row_group_background_color="#F8F9FA"
        )
    )

    return ui.HTML(tbl._repr_html_())
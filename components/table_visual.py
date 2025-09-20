from great_tables import GT, style, loc, md, nanoplot_options
from shiny import ui
import polars as pl
import numpy as np
import json

def table_display(df_sum, year, region):
    if df_sum.empty:
        return ui.div(
            "No data available for the selected filters.",
            style="text-align: center; padding: 20px; font-size: 16px;"
        )
    
    # Convert Pandas to Polars
    df_polars = pl.from_pandas(df_sum)

    region_display = region if region != "All" else "All Regions"

    # Create the table with enhanced styling
    tbl = (
        GT(df_polars)
        .tab_header(
            title=f"{region_display}, {year}",
            subtitle=" "
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
                "Elasticity Proxy": "Elasticity Proxy",
                "Discount Strategy": "Discount Strategy",
                "Revenue Trend (All Years)": "Revenue Trend"
            }
        )
        .cols_width(
            **{
                "Category_Display": "10%",
                "Sub-Category": "10%",
                "Rank": "5%",
                "Revenue": "8%",
                "Quantity": "8%",
                "Profit": "8%",
                "YoY Revenue %": "8%",
                "Discount": "8%",
                "Elasticity Proxy": "8%",
                "Discount Strategy": "17%",
                "Revenue Trend (All Years)": "10%"
            }
        )
        # Formatting
        .fmt_number(columns=["Revenue", "Profit"], compact=True, pattern="${x}", n_sigfig=3)
        .fmt_number(columns=["Quantity"], decimals=0)
        .fmt_number(columns=["Rank"], decimals=0)
        .fmt_percent(columns=["Discount"], decimals=1)
        .fmt_percent(columns=["YoY Revenue %"], decimals=1)
        
        # Trend sparkline with blue color
        .fmt_nanoplot(
            columns="Revenue Trend (All Years)", 
            options=nanoplot_options(
                data_point_radius=8,
                data_point_stroke_color="black",
                data_point_stroke_width=2,
                data_point_fill_color="white",
                data_line_type="straight",
                data_line_stroke_color="#1f77b4",  # Blue color
                data_line_stroke_width=2,
                data_area_fill_color="#6eaddd",
                vertical_guide_stroke_color="green",
            ),
        )
        # Missing values
        .sub_missing(missing_text="")
        
        # Alignment
        .tab_style(
            style=style.text(align="center"),
            locations=loc.body(columns=["Rank", "Revenue", "Quantity", "Profit", 
                                       "YoY Revenue %", "Discount", "Elasticity Proxy", "Discount Strategy", "Revenue Trend (All Years)"])
        )
        .tab_style(
            style=style.text(align="left"),
            locations=loc.body(columns=["Category_Display", "Sub-Category"])
        )
        .tab_style(
            style=style.text(align="center"),
            locations=loc.column_labels(columns=["Rank", "Revenue", "Quantity", "Profit", 
                                                "YoY Revenue %", "Discount", "Elasticity Proxy", "Discount Strategy",
                                                "Revenue Trend (All Years)"])
        )
        .tab_style(
            style=style.text(align="left"),
            locations=loc.column_labels(columns=["Category_Display", "Sub-Category"])
        )
        
        # Profit column formatting with gradient
        .data_color(
            columns=["Profit"],
            palette=["#ff6666", "#ffffff", "#66ff66"],  # Red to White to Green
            domain=[df_polars["Profit"].min(), df_polars["Profit"].max()],
            alpha=0.3  # Lower alpha for better text visibility
        )
        .fmt_currency(
            columns=["Profit"],
            currency="USD",
            pattern="{x}"
        )
        
        # Discount Strategy column styling
        .tab_style(
            style=style.text(size="12px"),  # Smaller font
            locations=loc.body(columns=["Discount Strategy"])
        )
        .tab_style(
            style=style.fill(color="#f1ebb1"),  
            locations=loc.body(columns=["Discount Strategy"])
        )
        .tab_style(
            style=style.borders(sides="all", color="#d0d0d0", style="solid", weight="1px"),
            locations=loc.body(columns=["Discount Strategy"])
        )
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(columns=["Discount Strategy"])
        )
        
        # Bold totals
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(rows=pl.col("Category_Display") == "Total")
        )
        # Column labels styling
        .tab_style(
            style=style.fill(color="#2C3E50"),
            locations=loc.column_labels()
        )
        .tab_style(
            style=style.text(color="white", weight="bold"),
            locations=loc.column_labels()
        )

        # Row group styling
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.row_groups()
        )

        # Table options
        .tab_options(
            table_width="100%",
            container_width="100%",
            table_font_size="1rem",
            row_group_background_color="#F8F9FA"
        )
    )

    return ui.HTML(tbl._repr_html_())
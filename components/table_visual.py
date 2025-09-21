from great_tables import GT, style, loc, md, nanoplot_options
from shiny import ui
import polars as pl

def table_display(df_sum, year, region):
    if df_sum.empty:
        return ui.div(
            "No data available for the selected filters.",
            style="text-align: center; padding: 20px; font-size: 16px;"
        )
    
    # Convert Pandas to Polars
    df_polars = pl.from_pandas(df_sum)

    # Preprocess the data to add symbols
    df_polars = df_polars.with_columns(
        (pl.col("YoY Revenue %") * 100).round(1).cast(pl.Utf8) + "%"
    )
    
    # Then add arrows based on the original value
    df_polars = df_polars.with_columns(
        pl.when(pl.col("YoY Revenue %").str.replace("%", "").cast(pl.Float64) > 0)
        .then("▲ " + pl.col("YoY Revenue %") )
        .otherwise( "▼" + pl.col("YoY Revenue %") )
        .alias("YoY Revenue %")
    )
    
    region_display = region if region != "All" else "All Regions"

    # Calculate profit min/max before the GT chain (moved here to fix syntax error)
    non_total_profits = df_polars.filter(pl.col("Category_Display") != "Total")["Profit"]
    profit_min = non_total_profits.min() 
    profit_max = non_total_profits.max() 

    # Create the table with enhanced styling
    tbl = (
        GT(df_polars) 
        .tab_header(
            title=f"Discount Strategy for {region_display}, {year}",
            subtitle=" "
        )
        .tab_spanner(label="Discount Strategy", columns=["Discount", "Elasticity Proxy", "Discount Strategy"])
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
        # Formatting
        .fmt_number(columns=["Revenue", "Profit"], compact=True, pattern="${x}", n_sigfig=3)
        .fmt_number(columns=["Quantity"], decimals=0)
        .fmt_number(columns=["Rank"], decimals=0)
        .fmt_percent(columns=["Discount"], decimals=1)
        
        
        # Color coding for YoY Revenue %
        .tab_style(
            style=style.text(color="green"),
            locations=loc.body(columns=["YoY Revenue %"], 
                             rows=pl.col("YoY Revenue %").str.contains("▲"))
        )
        .tab_style(
            style=style.text(color="red"),
            locations=loc.body(columns=["YoY Revenue %"], 
                             rows=pl.col("YoY Revenue %").str.contains("▼"))
        )
        
        # Trend sparkline with blue color
        .fmt_nanoplot(
            columns="Revenue Trend (All Years)", 
            options=nanoplot_options(
                data_point_radius=15,
                data_point_stroke_color="blue",
                data_point_stroke_width=4,
                data_point_fill_color="white",
                data_area_fill_color="blue",
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
        
        # Profit column formatting with gradient (excluding total row)
        .data_color(
            columns=["Profit"],
            palette=["#ff6666", "#ffffff", "#66ff66"],
            domain=[profit_min, profit_max],
            alpha=0.3
        )
        .fmt_number(
            columns=["Profit"],
            compact=True,
            pattern="${x}",
            n_sigfig=3
        )
        
        # Remove gradient from total row
        .tab_style(
            style=style.fill(color="white"),
            locations=loc.body(rows=pl.col("Category_Display") == "Total", columns="Profit")
        )
        
        # Discount Strategy column styling
        .tab_style(
            style=style.text(color="#A5A5A5", weight="bold"),  
            locations=loc.body(columns=["Discount Strategy"])
        )
        .tab_style(
            style=style.text(color="red"),
            locations=loc.body(columns=["Discount Strategy"], 
                             rows=pl.col("Discount Strategy").str.contains("Reduce discount"))
        )
        .tab_style(
            style=style.text(color="green"),
            locations=loc.body(columns=["Discount Strategy"], 
                             rows=pl.col("Discount Strategy").str.contains("Increase discount"))
        )

        # Total row styling
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(rows=pl.col("Category_Display") == "Total")
        )
        .tab_style(
            style=style.borders(sides="bottom", color="#a0a0a0", style="solid", weight="1px"),
            locations=loc.body(rows=pl.col("Category_Display") == "Total")
        )

        # Table options
        .tab_options(
            table_width="100%",
            container_width="100%",
            table_font_size="1rem",

            table_body_hlines_color="#eeeeee",
            table_body_hlines_style="solid",
            table_body_hlines_width="1px",

            heading_border_bottom_color="#ffffff",
            heading_border_bottom_width= "0px",
            
            column_labels_border_top_color="#cccccc",
            column_labels_border_top_width= "2px",

            column_labels_border_bottom_color="#cccccc",
            column_labels_border_bottom_width="2px",
            
            table_body_border_bottom_color= "#ffffff",
            table_body_border_top_color= "#ffffff",

            table_border_top_width= "0px"
        )
    )

    return ui.HTML(tbl._repr_html_())
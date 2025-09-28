from great_tables import GT, style, loc, md, nanoplot_options
from shiny import ui
import polars as pl

def table_display(df_sum, year, region):
    '''
    Render an interactive table displaying summarized sales data with enhanced styling and visualizations.

    This function transforms a summarized DataFrame into a polished Great Tables object, incorporating
    dynamic formatting, color coding, and sparklines to highlight discount strategies and performance
    metrics. It preprocesses data to add YoY revenue symbols, applies gradients for profit analysis,
    and ensures a clean, responsive layout focused on usability.

    Args:
        df_sum (pandas.DataFrame): A summarized DataFrame 
        year (str): The selected year for the analysis.
        region (str): The selected region (e.g., "All" or a specific region).

    Returns:
        shiny.ui.HTML: An HTML-rendered table object for display in a Shiny application.

    Example:
        >>> table_display(df_summary, "2023", "West")
        # Returns HTML table with styled metrics
    '''

    if df_sum.empty:
        return ui.div(
            "No data available for the selected filters.",
            style="text-align: center; padding: 20px; font-size: 16px;"
        )
    
    # Convert Pandas to Polars
    df_polars = pl.from_pandas(df_sum)

    # Preprocess the data to add symbols (adding '%' to YoY Revenue % column)
    df_polars = df_polars.with_columns(
        (pl.col("YoY Revenue %") * 100).round(1).cast(pl.Utf8) + "%"
    )
    
    # Adding conditional up and down arrows to the YoY Revenue % column
    df_polars = df_polars.with_columns(
        pl.when(pl.col("YoY Revenue %").str.replace("%", "").cast(pl.Float64) > 0)
        .then("▲ " + pl.col("YoY Revenue %") )
        .otherwise( "▼" + pl.col("YoY Revenue %") )
        .alias("YoY Revenue %")
    )
    
    region_display = region if region != "All" else "All Regions"

    # Calculate profit min/max 
    non_total_profits = df_polars.filter(pl.col("Category_Display") != "Total")["Profit"] # making sure to not include the total row
    profit_min = non_total_profits.min() 
    profit_max = non_total_profits.max() 

    # Create the table with enhanced styling
    tbl = (
        GT(df_polars) 
        .tab_header(
            title=f"Discount Strategy for {region_display}, {year}", # title
            subtitle=" "
        )
        .tab_spanner(label="Discount Strategy", columns=["Discount", "Elasticity Proxy", "Discount Strategy"]) # underlying border for the specified columns in Discount Strategy
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
            locations=loc.body(columns=["YoY Revenue %"],  rows=pl.col("YoY Revenue %").str.contains("▲"))
        )
        .tab_style(
            style=style.text(color="red"),
            locations=loc.body(columns=["YoY Revenue %"], rows=pl.col("YoY Revenue %").str.contains("▼"))
        )
        
        # Trend sparkline with blue color
        .fmt_nanoplot(
            columns="Revenue Trend (All Years)", 
            options=nanoplot_options(
                data_point_radius=15, #size of markers
                data_point_stroke_color="#3B82F6",
                data_point_stroke_width=4,
                data_point_fill_color="white",
                data_area_fill_color="#3B82F6",
            ),
        )
        # Missing values
        .sub_missing(missing_text="")
        
        # Alignment
        .tab_style(
            style=style.text(align="center"),
            locations=loc.body(columns=["Rank", "Revenue", "Quantity", "Profit", 
                                       "YoY Revenue %", "Discount", "Elasticity Proxy", "Discount Strategy", "Revenue Trend (All Years)"]) #center-aligned
        )
        .tab_style(
            style=style.text(align="left"),
            locations=loc.body(columns=["Category_Display", "Sub-Category"]) #left-aligned
        )
        .tab_style(
            style=style.text(align="center"),
            locations=loc.column_labels(columns=["Rank", "Revenue", "Quantity", "Profit", 
                                                "YoY Revenue %", "Discount", "Elasticity Proxy", "Discount Strategy",
                                                "Revenue Trend (All Years)"]) # this time for their column labels, we did it for their body
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
            style=style.text(color="#A5A5A5", weight="bold"), #for maintain discount
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
            style=style.text(weight="bold"), # bold
            locations=loc.body(rows=pl.col("Category_Display") == "Total")
        )
        .tab_style(
            style=style.borders(sides="bottom", color="#a0a0a0", style="solid", weight="1px"),
            locations=loc.body(rows=pl.col("Category_Display") == "Total") # dark border at bottom
        )

        # Table options
        # Modifying the overall color and border size of the table to have a more minimalistic view
        .tab_options(
            table_width="100%",
            container_width="100%",
            table_font_size="1rem",

            table_body_hlines_color="#f5f5f5",
            table_body_hlines_style="solid",
            table_body_hlines_width="1px",

            heading_border_bottom_color="#a0a0a0",
            heading_border_bottom_width= "1px",
            
            column_labels_border_top_color="#a0a0a0",
            column_labels_border_top_width= "1px",

            column_labels_border_bottom_color="#a0a0a0",
            column_labels_border_bottom_width="1px",
            
            table_body_border_bottom_color= "#ffffff",
            table_border_top_color= "#ffffff"    

        )
    )

    return ui.HTML(tbl._repr_html_())
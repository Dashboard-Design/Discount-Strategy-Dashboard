from great_tables import GT, style, loc
from shiny import ui

def table_display(df_sum, year, region):
    if df_sum.empty:
        return ui.div(
            "No data available for the selected filters.",
            style="text-align: center; padding: 20px; font-size: 16px;"
        )

    region_display = region if region != "All" else "All Regions"

    tbl = (
        GT(df_sum)
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
                "Profit": "Profit",
                "YoY Revenue %": "YoY Revenue %",
                "YoY Profit %": "YoY Profit %",
                "Discount %": "Discount %"
            }
        )
        # No formatting needed since values are already formatted inline
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
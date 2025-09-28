# Discount Strategy Dashboard
An interactive business intelligence dashboard built with Quarto and Shiny with Python that serves as a sophisticated decision-making tool for optimizing discount strategies based on complex business logic and price elasticity analysis.

<img width="7684" height="4322" alt="Image" src="https://github.com/user-attachments/assets/8b92cf32-af2b-4b0d-97b7-707f101fb00e" />

## Overview
This dashboard transforms complex sales data into actionable discount optimization insights. 
It enables businesses to make data-driven decisions on discount strategies by analyzing multiple dimensions including price elasticity, customer segments, regional performance, and historical trends.

## Live Dashboard
Access the live decision-making tool here:
https://sajjadahmadi-discount-strategy-dashboard.share.connect.posit.cloud/

## Analytics
- Price Elasticity Analysis: Calculates customer sensitivity to price changes across product categories
- Strategic Discount Optimization: Recommends optimal discount levels (Increase/Reduce/Maintain) based on complex business rules
- Revenue Impact: Projects how discount changes affect overall profitability
- Segment-Specific Strategies: Tailors recommendations for different customer priorities (New Customers, High-Value Accounts, etc.)
- Regional Insights: Analyzes performance across different geographic locations
- Historical Trends: Visualizes past discount strategies and their outcomes

## Architecture & Technology
Core Framework
- Quarto: Modern publishing system for analytical dashboards
- Shiny for Python: Interactive web application framework
- Custom CSS and JavaScript: Enhanced UI/UX

## Basic Operation
1. Select the target year using the year filter
2. Choose the region for analysis (All Regions or specific region)
3. Set company strategic goals
4. Select customer priority segments
5. Review the generated discount strategy recommendations

## Interpreting Results
- Elasticity Scores: Values closer to 1 indicate price-sensitive categories
- Strategy Recommendations: Based on elasticity, growth trends, and strategic goals
- Performance Metrics: Revenue, quantity, profit, and year-over-year growth


## Setup Instructions
1. Clone the repository
2. Install Quarto CLI
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run the dashboard locally: `quarto preview dashboard.qmd`
5. Open your browser to the local server address

## Deploy on Posit Cloud
1. For deploying on https://connect.posit.cloud/ 
2. Run `quarto render --output-dir _build`
3. Select shiny server
4. Choose app.py in _build folder as main python file

## Data Source
- dataset provided in `/dataset/sample_-_superstore.csv`

## Code Structure
- `dashboard.qmd` - Main dashboard with table rendering
- `components/table_logic.py` - Data processing logic
- `components/table_visual.py` using great table to visualize the table
- Custom CSS/JS for enhanced functionality in the navbar-filter.lua and styles.css

## Table Methodology
The main table uses Great Tables library with:
- Conditional formatting based on business rules
- Dynamic filtering based on user inputs
- Custom styling for better readability
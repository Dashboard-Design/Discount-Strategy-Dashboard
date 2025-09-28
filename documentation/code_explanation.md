# Code Explanation - Discount Strategy Dashboard

## Overview
This dashboard provides data-driven discount strategy recommendations by analyzing sales data across multiple dimensions including price elasticity, customer segments, regional performance, and historical trends.

## Project Structure
```text
dataset/
├── samples_-_superstore.xls
components/
├── Discount_logic.py     # Core business logic for discount recommendations
├── table_logic.py        # Data processing and aggregation
└── table_visual.py       # Table visualization with Great Tables
styles.css                # Custom styling and theming
Dashboard.qmd             # Main Quarto dashboard file
navbar-filter.lua         # Modifying css and javascript of modal view and navbar for quarto dashboard
```

## Core Components

1. Discount Logic (Discount_logic.py)
Purpose: Implements the core business logic for discount strategy recommendations.

Key Functions:
- discount_strategy(): Calculates optimal discount strategy using a scoring system

Business Rules:
- Revenue Impact: Higher revenue products get positive scores
- Profit Protection: Low-profit products get negative scores
- Market Context: Considers inflation and competitor pricing
- Strategic Goals: Adjusts scores based on company objectives
- Customer Segments: Tailors recommendations for different customer types

Scoring System:
- Score ≥ 4: "Increase discount"
- Score ≤ -1: "Reduce discount"
- Otherwise: "Maintain discount"

2. Data Processing (table_logic.py)
Purpose: Aggregates and processes raw sales data into analytical metrics.

Key Functions:

- summary(): Main data processing pipeline

Processing Steps:

- 1. Base Aggregation:
```python
# Groups by Category/Sub-Category and calculates metrics
Revenue = Sales sum
Profit = Profit sum  
Discount = Discount average
Quantity = Quantity sum
```

- 2. Year-over-Year Growth:
```python
# Compares current year with previous year
YoY Revenue % = (Current Revenue - Previous Revenue) / Previous Revenue
```

- 3. Revenue Trend Analysis:
```python
# Creates sparkline data for visualization
"Revenue Trend (All Years)" = Space-separated revenue values for all years
```

- 4. Elasticity Proxy:
```python
# Measures price sensitivity using correlation
Elasticity Proxy = Correlation(Discount, Revenue) across years
```

- 5. Ranking & Categorization:
```python
# Ranks sub-categories within each category by revenue
Rank = Revenue ranking within category
```


3. Table Visualization (table_visual.py)
Purpose: Transforms processed data into a polished, interactive table.

Key Features:

Great Tables Integration: Uses the great_tables library for advanced table formatting

Visual Enhancements:

Sparklines for revenue trends

Color-coded YoY growth indicators (▲ green, ▼ red)

Profit gradient coloring

Custom styling for discount strategy recommendations

Responsive Design: Adapts to different screen sizes

Styling Elements:

Profit gradient from red (low) to green (high)

Strategic color coding for discount recommendations

Professional table formatting with proper alignment

4. Dashboard Integration (Dashboard.qmd)
Purpose: Main application file that integrates all components.

Key Sections:

Setup & Data Loading:

python
# Loads Superstore dataset and prepares filter options
df = pd.read_excel("dataset/sample_-_superstore.xls")
Reactive Components:

Region and Year filters

Company goal and customer priority selectors

Real-time data processing

Layout Structure:

Sidebar with filters and information

Main content area with the discount strategy table

Data Flow
text
Raw Data → Filtering → Aggregation → Business Logic → Visualization
    ↓          ↓           ↓             ↓               ↓
Superstore → Region/Year → Summary → Discount Logic → Great Tables
Key Business Metrics
Calculated Metrics:
Revenue: Total sales per sub-category

Profit: Net profit per sub-category

YoY Revenue %: Year-over-year growth percentage

Discount %: Average discount applied

Elasticity Proxy: Price sensitivity indicator (-1 to 1)

Rank: Performance ranking within category

Strategic Inputs:
Company Goals: Revenue Growth, Profit Protection, Market Share Expansion, Customer Retention

Customer Priorities: New Customers, Loyal Customers, High-Value Accounts, All Segments

Custom Styling (styles.css)
Design Philosophy: Clean, professional, data-focused interface

Key Features:

Minimalist color scheme with strategic color coding

Custom classes for discount decisions and elasticity indicators

Responsive layout adjustments

Hidden download functionality for data export

Deployment
The dashboard is deployed on Posit Cloud and includes:

Interactive filtering capabilities

Real-time calculations

Professional business presentation

Data export functionality

Reproducibility
To reproduce this dashboard:

Install dependencies from requirements.txt

Place Superstore dataset in dataset/ folder

Run quarto preview Dashboard.qmd

All processing steps are contained within the provided code files
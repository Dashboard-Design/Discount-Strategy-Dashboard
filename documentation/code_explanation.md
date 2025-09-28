# Discount Strategy Dashboard

## 📋 Overview

The Discount Strategy Dashboard is a comprehensive data analytics tool that provides data-driven discount strategy recommendations by analyzing sales data across multiple dimensions. The system evaluates price elasticity, customer segments, regional performance, and historical trends to deliver actionable business insights.

## 🏗️ Project Structure

```
discount-strategy-dashboard/
├── dataset/
│   └── samples_-_superstore.xls        # Source data file
├── components/
│   ├── Discount_logic.py                # Core business logic for recommendations
│   ├── table_logic.py                   # Data processing and aggregation
│   └── table_visual.py                  # Table visualization with Great Tables
├── styles.css                           # Custom styling and theming
├── Dashboard.qmd                        # Main Quarto dashboard file
├── navbar-filter.lua                    # CSS/JS modifications for Quarto
└── requirements.txt                     # Python dependencies
```

## 🧩 Core Components

### 1. Discount Logic (`Discount_logic.py`)

**Purpose:** Implements the core business logic for discount strategy recommendations using a sophisticated scoring system.

**Key Functions:**
- `discount_strategy()` - Calculates optimal discount strategy using weighted scoring

**Business Rules:**
- **Revenue Impact:** Higher revenue products receive positive scores
- **Profit Protection:** Low-profit products receive negative scores  
- **Market Context:** Considers inflation and competitor pricing dynamics
- **Strategic Goals:** Adjusts scores based on company objectives
- **Customer Segments:** Tailors recommendations for different customer types

**Scoring System:**
```
Score ≥ 4   → "Increase discount"
Score ≤ -1  → "Reduce discount"
Otherwise   → "Maintain discount"
```

### 2. Data Processing (`table_logic.py`)

**Purpose:** Aggregates and processes raw sales data into analytical metrics for business intelligence.

**Key Functions:**
- `summary()` - Main data processing pipeline

**Processing Pipeline:**

#### Step 1: Base Aggregation
```python
# Groups by Category/Sub-Category and calculates core metrics
Revenue = sum(Sales)
Profit = sum(Profit)  
Discount = mean(Discount)
Quantity = sum(Quantity)
```

#### Step 2: Year-over-Year Growth Analysis
```python
# Compares current year performance with previous year
YoY_Revenue_% = (Current_Revenue - Previous_Revenue) / Previous_Revenue * 100
```

#### Step 3: Revenue Trend Analysis
```python
# Creates sparkline data for time series visualization
Revenue_Trend = "space-separated revenue values for all years"
```

#### Step 4: Price Elasticity Calculation
```python
# Measures price sensitivity using statistical correlation
Elasticity_Proxy = correlation(Discount, Revenue) across years
# Range: -1 (highly elastic) to +1 (inelastic)
```

#### Step 5: Performance Ranking
```python
# Ranks sub-categories within each category by revenue performance
Rank = revenue_ranking_within_category
```

### 3. Table Visualization (`table_visual.py`)

**Purpose:** Transforms processed data into a polished, interactive business table using advanced formatting.

**Key Features:**
- **Great Tables Integration:** Utilizes the `great_tables` library for professional table formatting
- **Visual Enhancements:**
  - Sparklines for revenue trend visualization
  - Color-coded YoY growth indicators (▲ green for growth, ▼ red for decline)
  - Profit gradient coloring from red (low) to green (high)
  - Strategic color coding for discount recommendations
- **Responsive Design:** Adapts seamlessly to different screen sizes
- **Interactive Elements:** Hover effects with CSS modification

### 4. Dashboard Integration (`Dashboard.qmd`)

**Purpose:** Main Quarto application file that orchestrates all components into a cohesive dashboard.

**Key Sections:**

#### Setup & Data Loading
```python
# Loads Superstore dataset and initializes filter options
df = pd.read_excel("dataset/sample_-_superstore.xls")
```

#### Reactive Components on Sidebar
- **Geographic Filters:** Region selection
- **Temporal Filters:** Year range selection  
- **Strategic Inputs:** Company goal and customer priority selectors

#### Layout Structure
- **Sidebar:** Interactive filters and contextual information
- **Main Content:** Discount strategy table with business insights

## 🔄 Data Flow Architecture

```
Raw Data → Filtering → Aggregation , Business Logic → Visualization
          
Superstore → Region/Year → Summary , Discount Logic → Great Tables
```

## 📊 Key Business Metrics

### Calculated Metrics
| Metric | Description | Business Value |
|--------|-------------|----------------|
| **Revenue** | Total sales per sub-category | Primary performance indicator |
| **Profit** | Net profit per sub-category | Profitability assessment |
| **YoY Revenue %** | Year-over-year growth percentage | Growth trend analysis |
| **Discount %** | Average discount applied | Pricing strategy effectiveness |
| **Elasticity Proxy** | Price sensitivity indicator (-1 to 1) | Demand responsiveness |
| **Rank** | Performance ranking within category | Competitive positioning |

### Strategic Inputs

#### Company Goals
- 🚀 **Revenue Growth:** Focus on market expansion
- 💰 **Profit Protection:** Emphasize margin preservation  
- 📈 **Market Share Expansion:** Competitive positioning priority
- 🎯 **Customer Retention:** Loyalty-focused strategy

#### Customer Priorities
- 🆕 **New Customers:** Acquisition-focused discounting
- 💎 **Loyal Customers:** Retention and reward strategies
- 💼 **High-Value Accounts:** Premium customer treatment
- 🌐 **All Segments:** Balanced approach across customer base

## 🎨 Custom Styling (`styles.css`)

**Design Philosophy:** Clean, professional, data-focused interface optimized for business users.

**Key Features:**
- **Color Scheme:** Minimalist palette with strategic color coding
- **Custom Classes:** Specialized styling for discount decisions and elasticity indicators
- **Responsive Layout:** Mobile-friendly design adjustments
- **Export Functionality:** Hidden download capabilities for data export
- **Typography:** Professional fonts optimized for data readability

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- Quarto CLI
- Git

### Local Development
```bash
# 1. Clone the repository
git clone <repository-url>
cd discount-strategy-dashboard

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Quarto CLI (if not already installed)
# Visit: https://quarto.org/docs/get-started/

# 4. Run the dashboard locally
quarto preview Dashboard.qmd

# 5. Open your browser to the displayed local server address
```

## 🌐 Deployment

### Posit Cloud Deployment

1. **Prepare for deployment:**
   ```bash
   quarto render --output-dir _build
   ```

2. **Deploy to Posit Cloud:**
   - Navigate to [https://connect.posit.cloud/](https://connect.posit.cloud/)
   - Create new project
   - Select **Shiny Server** as deployment type
   - Choose `app.py` in `_build` folder as main Python file
   - Configure environment settings
   - Deploy application

3. **Post-deployment:**
   - Monitor application logs
   - Configure access permissions


## 📝 Usage Guidelines

1. **Filter Selection:** Use sidebar filters to narrow analysis scope
2. **Strategy Interpretation:** Focus on "Discount Strategy" column for actionable insights
3. **Trend Analysis:** Utilize sparklines for quick trend identification
4. **Export Data:** Use built-in export functionality for further analysis
5. **Regular Updates:** Refresh data periodically for current insights

---

*Last updated: 9/28/2025
*Version: 1.0.0*
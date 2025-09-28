discount_policy = {
    "high_revenue": 70000,
    "low_revenue": 30000,
    "high_profit": 6500,
    "low_profit": 4000,
    "min_discount": 0.1,
    "max_discount": 0.2,
}

market_context = {
    "inflation_rate": 0.06,          # 6%
    "competitor_discount": 0.15    # competitor offering
}


def discount_strategy(row, company_goal, customer_priority, policy=discount_policy, context=market_context ):
    '''
    Determine the optimal discount strategy based on revenue, profit, YoY growth,
    discount levels, company goals, customer priorities, and market context.

    This function evaluates various financial and strategic factors to recommend
    whether to increase, reduce, or maintain discounts. It uses a scoring system
    influenced by policy thresholds, external market conditions, and business objectives.

    Args:
        row (pandas.DataFrame): A dataframe containing original data with keys "Revenue", "Profit", "YoY Revenue %", and "Discount" columns.
        company_goal (str): The company's strategic focus, for example "Revenue Growth".
        customer_priority (str): The target customer segment, for example "New Customers".
        policy (dict, optional): A dictionary of policy thresholds.
        context (dict, optional): A dictionary of market context data.

    Returns:
        str: An HTML-formatted string with a class indicating the strategy:
             - '<span class="decision-increase">Increase discount</span>' for score >= 4
             - '<span class="decision-reduce">Reduce discount</span>' for score <= -1
             - '<span class="decision-maintain">Maintain discount</span>' otherwise.
    '''

    score = 0
    
    rev, profit, yoy, disc = (
        row["Revenue"],
        row["Profit"],
        row["YoY Revenue %"],
        row["Discount"],
    )
    
    # Revenue contribution
    if rev > policy["high_revenue"]:
        score += 2
    elif rev < policy["low_revenue"]:
        score -= 1
    
    # Profit margin effect
    if profit < policy["low_profit"]:
        score -= 2
    else:
        score += 1
    
    # Discount level
    if disc < policy["min_discount"]:
        score += 1
    elif disc > policy["max_discount"]:
        score -= 1
    
    # External context
    if context["inflation_rate"] > 0.05:
        score -= 1
    if context["competitor_discount"] > disc:
        score += 2
    
    # Company goal adjustment
    if company_goal == "Revenue Growth" and yoy > 0:
        score += 2
    elif company_goal == "Profit Protection" and profit < policy["low_profit"]:
        score -= 2
    elif company_goal == "Market Share Expansion":
        score += 1  # slightly more generous overall
    elif company_goal == "Customer Retention" and customer_priority == "Loyal Customers":
        score += 2
    
    # Customer segment adjustment
    if customer_priority == "New Customers":
        score += 1  # encourage capturing them with a bit more discount
    elif customer_priority == "High-Value Accounts" and profit > policy["high_profit"]:
        score += 2  # reward discounts for strategic accounts
    elif customer_priority == "Loyal Customers" and yoy <= 0:
        score += 1  # encourage keeping them engaged
    else:
        score += 0    
    
    # Strategy decision with HTML + classes
    if score >= 4:
        return '<span class="decision-increase">Increase discount</span>'
    elif score <= -1:
        return '<span class="decision-reduce">Reduce discount</span>'
    else:
        return '<span class="decision-maintain">Maintain discount</span>'
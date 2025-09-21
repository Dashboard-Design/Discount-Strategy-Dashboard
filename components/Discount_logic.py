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
    score = 0
    
    rev, profit, yoy, disc = (
        row["Revenue_num"],
        row["Profit_num"],
        row["YoY Revenue %"],
        row["Discount_num"],
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
    
    # Strategy decision
    if score >= 4:
        return "Increase discount"
    elif score <= -2:
        return "Reduce discount"
    else:
        return "Maintain discount"

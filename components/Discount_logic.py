import pandas as pd

# Discount Strategy Logic

def discount_strategy(row):
        rev, profit, qty, yoy, disc = row["Revenue_num"], row["Profit_num"], row["Quantity"], row["YoY Revenue %"], row["Discount_num"]
        if pd.isna(yoy): 
            return "No prior year data"
        if rev > 50000 and profit > 5000 and disc < 0.1:
            return "Potential to Grow: increase discount slightly"
        elif rev > 50000 and profit < 2000 and disc > 0.2:
            return "Discount hurting margins: decrease discount"
        elif rev < 20000 and disc > 0.2 and yoy <= 0:
            return "Ineffective discounting: reduce discount"
        elif rev < 20000 and disc < 0.1 and yoy > 0:
            return "Emerging product: consider increasing discount"
        else:
            return "Maintain current discount"
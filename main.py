import pandas as pd


data = pd.read_csv("data.csv")

data["Revenue_Growth"] = data["Revenue"].pct_change() * 100

data["Profit_Margin"] = (
    data["Net_Income"] / data["Revenue"]
) * 100

data["Debt_Growth"] = data["Debt"].pct_change() * 100

print(data)

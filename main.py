import pandas as pd


# Load the financial data.
data = pd.read_csv("data.csv")

data["Revenue_Growth"] = data["Revenue"].pct_change() * 100


print(data)
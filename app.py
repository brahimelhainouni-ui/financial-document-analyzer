import streamlit as st
import pandas as pd


st.title("Financial Document Analyzer")

st.write("Analyze financial data and calculate key financial metrics.")


data = pd.read_csv("data.csv")
data["Revenue_Growth"] = data["Revenue"].pct_change() * 100
data["Profit_Margin"] = (
    data["Net_Income"] / data["Revenue"]
) * 100
data["Debt_Growth"] = data["Debt"].pct_change() * 100

st.subheader("Financial Data")

st.dataframe(data)

st.subheader("Key Metrics")

latest_year = data.iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Revenue",
    f"€{latest_year['Revenue']:,.0f}"
)

col2.metric(
    "Net Income",
    f"€{latest_year['Net_Income']:,.0f}"
)

col3.metric(
    "Profit Margin",
    f"{latest_year['Profit_Margin']:.2f}%"
)

import streamlit as st
import pandas as pd
import ollama
from pathlib import Path


# Page configuration
st.set_page_config(
    page_title="Financial Document Analyzer",
    page_icon="📊",
    layout="wide"
)


# Load financial data
@st.cache_data
def load_data():
    file_path = Path(__file__).parent / "data.csv"
    data = pd.read_csv(file_path)

    required_columns = [
        "Year",
        "Revenue",
        "Net_Income",
        "Debt"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing column: {column}")

    for column in required_columns:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

    data = data.dropna(subset=required_columns)
    data = data.sort_values("Year").reset_index(drop=True)

    if data.empty:
        raise ValueError("The CSV file contains no valid data.")

    data["Revenue_Growth"] = (
        data["Revenue"].pct_change() * 100
    )

    data["Profit_Margin"] = (
        data["Net_Income"]
        / data["Revenue"].where(data["Revenue"] != 0)
    ) * 100

    data["Debt_Growth"] = (
        data["Debt"].pct_change() * 100
    )

    return data


def generate_ai_analysis(data):

    financial_data = data.round(2).to_string(index=False)

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": """
                You are a financial data analyst.

                Analyze the provided financial data.
                Explain:
                1. Revenue development
                2. Profit margin
                3. Debt development
                4. Potential risks and opportunities

                Use only the provided figures.
                Do not invent financial information.
                Write in clear and professional English.
                """
            },
            {
                "role": "user",
                "content": (
                    "Analyze the following financial data:\n"
                    + financial_data
                )
            }
        ]
    )

    return response["message"]["content"]
# Dashboard title
st.title("📊 Financial Document Analyzer")

st.write(
    "Analyze financial data and monitor important "
    "financial performance indicators."
)


# Handle loading errors
try:
    data = load_data()

except FileNotFoundError:
    st.error("The file data.csv could not be found.")
    st.stop()

except (ValueError, pd.errors.ParserError) as error:
    st.error(f"Could not load financial data: {error}")
    st.stop()


# Latest financial metrics
latest_year = data.iloc[-1]

st.subheader(f"Key Metrics – {int(latest_year['Year'])}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue",
    f"€{latest_year['Revenue']:,.0f}",
    delta=(
        f"{latest_year['Revenue_Growth']:.2f}%"
        if pd.notna(latest_year["Revenue_Growth"])
        else None
    )
)

col2.metric(
    "Net Income",
    f"€{latest_year['Net_Income']:,.0f}"
)

col3.metric(
    "Profit Margin",
    (
        f"{latest_year['Profit_Margin']:.2f}%"
        if pd.notna(latest_year["Profit_Margin"])
        else "N/A"
    )
)

col4.metric(
    "Debt",
    f"€{latest_year['Debt']:,.0f}"
)


# Financial data table
st.subheader("Financial Data")

st.dataframe(
    data,
    use_container_width=True,
    hide_index=True
)


# Revenue and income chart
st.subheader("Revenue and Net Income Development")

chart_data = data.set_index("Year")[
    ["Revenue", "Net_Income"]
]

st.line_chart(chart_data)


# Profit margin chart
st.subheader("Profit Margin Development")

margin_data = data.set_index("Year")[["Profit_Margin"]]

st.line_chart(margin_data)


# Debt development
st.subheader("Debt Development")

debt_data = data.set_index("Year")[["Debt"]]

st.line_chart(debt_data)

# AI Financial Analysis

st.subheader("AI Financial Analysis")

st.write(
    "Generate an AI-powered analysis of your financial data "
    "using a local LLM."
)

if st.button("Generate AI Financial Analysis"):

    with st.spinner("Analyzing financial data..."):

        try:
            analysis = generate_ai_analysis(data)

            st.success("Analysis completed!")

            st.markdown(analysis)

        except Exception as error:
            st.error(
                f"Could not generate analysis: {error}"
            )

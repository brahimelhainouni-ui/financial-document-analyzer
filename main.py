
import pandas as pd
import ollama


def load_financial_data(file_path="data.csv"):
    """Load and calculate financial metrics."""

    data = pd.read_csv(file_path)

    required_columns = [
        "Revenue",
        "Net_Income",
        "Debt"
    ]

    for column in required_columns:
        if column not in data.columns:
            raise ValueError(f"Missing column: {column}")

        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

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


def generate_ai_analysis(data, model="llama3.2:3b"):

    summary = data.round(2).to_string(index=False)

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": """
                You are a financial analyst.
                Analyze revenue growth, profit margins
                and debt development.
                Identify risks and opportunities.
                Never invent financial figures.
                """
            },
            {
                "role": "user",
                "content": f"Analyze this financial data:\n{summary}"
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":

    data = load_financial_data()

    print("\nFINANCIAL DATA")
    print(data)

    print("\nAI FINANCIAL ANALYSIS")
    print(generate_ai_analysis(data))

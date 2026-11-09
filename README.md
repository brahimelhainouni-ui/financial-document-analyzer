# Financial Document Analyzer

A simple Python application that uses Pandas to analyze financial data and Streamlit to display the results. The application calculates financial metrics such as revenue growth, profit margin, and debt growth. I'm also working on integrating a local LLM with Ollama to generate financial summaries without using paid APIs.

Technologies:

Python, Pandas, Streamlit, Ollama, Llama 3.2.

Installation:

1. Clone the repository

```bash
git clone https://github.com/brahimelhainouni-ui/financial-document-analyzer.git

cd financial-document-analyzer
```

2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Git Bash:

```bash
source venv/Scripts/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Install the local AI model

Make sure Ollama is installed and running.

```bash
ollama pull llama3.2:3b
```

Run the Application:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

Then:

- View the financial data.
- Check the calculated financial metrics.
- Explore the dashboard.

Project Goal:

This project is part of my practical learning in:

- Python programming
- Financial data analysis
- Data processing with Pandas
- Streamlit web applications
- Local LLM integration using Ollama
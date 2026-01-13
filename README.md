# Trade Bot Analysis
### RAG-Powered Notebook for Financial Holdings & Trades Data

This repository contains a comprehensive **Retrieval-Augmented Generation (RAG)** implementation within a Jupyter Notebook to analyze financial datasets (`holdings.csv` and `trades.csv`).

The system is engineered to answer complex analytical questions about fund performance, holdings, and trades while strictly adhering to data-driven guardrails.

---

## Core Architecture

The bot uses a specialized RAG architecture designed for financial accuracy:

### 1. Dual-Document Retrieval
- **Raw Documents**: Granular records for specific lookups (e.g., "P&L for security X").
- **Summary Documents**: Pre-computed aggregations (Total Holdings, Total Trades, Yearly P&L, Performance Rankings).
- **Zero-Count Handling**: Explicit "0" summaries are created for funds with no activity to prevent retrieval "hallucinations."

### 2. Conversational Intelligence
- **Query Condensation**: Rephrases follow-up questions (e.g., "Total trades for **that fund**") into standalone queries (e.g., "Total trades for **Garfield fund**") using chat history before retrieval.
- **Context Isolation**: Validates retrieved documents against the fund mentioned in the query using metadata filtering.

### 3. Guardrail System
- **Intent Routing**: Automatically routes queries to either summary or raw documents based on aggregation intent.
- **Strict Refusal**: Returns exactly `Sorry can not find the answer` if the information is unavailable or out-of-scope.
- **Deterministic Generation**: Uses GPT-4 with `temperature=0` to ensure consistency.

---

## Data Preprocessing

- **Schema Alignment**: Standardizes `PortfolioName` to `FundName` across datasets.
- **Temporal Analysis**: Extracts `Year` from `AsOfDate` for year-over-year comparisons.
- **Contextual Merging**: Joins holdings and trades on a composite key of `["SecurityId", "FundName"]`.

---

## Getting Started

### 1. Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 2. Set API Key
Ensure your OpenAI API key is set in your environment:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. Running the Analysis
Open and run the notebook:
```bash
jupyter notebook trade_bot.ipynb
```

---

## Evaluation Suite
The notebook includes an evaluation cell with 10+ varied test cases (Performance comparisons, Aggregations, Specific lookups, and Out-of-scope queries) to verify the bot's accuracy and safety metrics.

---

## Author
**Sagnik Mukherjee**  
GitHub: [sagnik0712mukherjee](https://github.com/sagnik0712mukherjee)

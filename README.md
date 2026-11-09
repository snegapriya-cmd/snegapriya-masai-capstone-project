# Swiggy Instamart Customer Intelligence Co-Pilot

## Project overview
This capstone demonstrates a customer intelligence workflow for a quick-commerce business. It combines data preparation, RFM-based customer segmentation, a basic churn-risk indicator, support-ticket classification, and a policy retrieval chatbot demonstration.

> **Data notice:** This repository generates synthetic, fictional demonstration data. It is not official Swiggy data and does not represent Swiggy's internal systems, policies, or model performance.

## Business objectives
- Prepare consistent customer, order and support-ticket data.
- Segment customers using Recency, Frequency and Monetary (RFM) features.
- Identify a simple at-risk group using recency as a proxy (not a validated churn model).
- Classify support tickets and route them to a suggested support team.
- Retrieve relevant sample policy text for customer questions.

## Project structure
```text
Swiggy_Instamart_Customer_Intelligence_Copilot/
├── data/                 # Generated CSV datasets
├── outputs/              # Analysis results
├── src/pipeline.py       # Cleaning, SQLite, RFM, clustering, NLP and retrieval
├── generate_data.py      # Creates synthetic source data
├── triage.py             # Ticket classification entry point
├── mock_llm.py           # Offline policy-question demo
├── run_project.py        # Runs all project stages
├── requirements.txt      # Python dependencies
└── README.md
```

## Technology stack
Python, Pandas, NumPy, SQLite, scikit-learn, TF-IDF, Logistic Regression, K-Means, PCA.

## Setup
Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the project
From the repository root:

```bash
python run_project.py
```

The script generates CSV files, cleans the data, stores tables in `Instamart_DB.sqlite`, performs RFM segmentation and ticket classification, and writes results to `outputs/`.

To test the policy retrieval demo:

```bash
python mock_llm.py
```

Example question: `How do I get a refund for a cancelled order?`

## Methodology
### Part A — Data foundation
Synthetic CSVs are generated for customers, orders, tickets and policy text. The pipeline standardizes text fields, removes duplicate records, handles invalid order amounts and missing join keys, and loads cleaned tables into SQLite.

### Part B — Customer analytics
RFM features are calculated from completed orders:
- **Recency:** days since the customer's latest completed order.
- **Frequency:** number of completed orders.
- **Monetary:** total completed-order spend.

StandardScaler normalizes the features before K-Means clustering. PCA reduces the scaled features to two components for exploratory visualization/variance analysis. A simple recency-quartile flag highlights customers who may need attention. This flag is a heuristic, not a trained churn prediction model.

### Part C — Support ticket triage
TF-IDF converts ticket text into numerical features. Logistic Regression predicts an issue category. A routing map suggests the team that should handle each ticket. Accuracy is measured on a held-out test set.

### Part D — Policy retrieval / RAG demonstration
The offline demo uses keyword overlap to retrieve a relevant sample policy paragraph. `mock_llm.py` simulates the response layer without an external LLM or API. A production RAG system would require approved policy documents, embeddings/vector search, an LLM, access controls, and human escalation.

## Outputs
- `data/*_clean.csv` — cleaned datasets
- `Instamart_DB.sqlite` — SQLite database
- `outputs/customer_segments.csv` — RFM values, clusters, PCA coordinates and risk heuristic
- `outputs/ticket_triage_results.csv` — predicted issue and routing team
- `outputs/run_summary.txt` — execution summary

## Limitations and future improvements
- Use consented, real, anonymized business data for a real deployment.
- Train and evaluate a true churn model using a clearly defined future churn label and time-based validation.
- Improve ticket classification with more varied, human-labelled examples and class-wise metrics.
- Replace keyword retrieval with embeddings/vector search and an approved LLM-backed RAG architecture.
- Connect order status and refunds only through secure, authorized APIs; never promise a refund based only on a chatbot response.

## Learning outcomes
Data cleaning, exploratory customer analytics, RFM, unsupervised learning, PCA, text classification, SQLite integration, retrieval concepts, reproducible project organization and GitHub documentation.

# LLM-Powered Financial Risk Explainer

A production-grade system for loan default risk prediction with explainable AI (SHAP) and natural language explanations powered by LLMs (OpenAI).

## 🚀 Overview

This project provides an end-to-end solution for financial institutions to not only predict loan default risk but also provide transparent, compliance-friendly explanations for both internal risk analysts and external customers.

### Key Features
- **Production ML Pipeline**: Modular training and evaluation with XGBoost, Random Forest, and Logistic Regression.
- **Explainable AI (XAI)**: Integrated SHAP for local and global feature importance.
- **LLM Explanations**: Automated generation of natural language summaries, risk drivers, and recommendations using GPT-4.
- **Risk Analyst Copilot**: Interactive Q&A for deep-diving into specific loan decisions.
- **MLOps Ready**: MLflow for experiment tracking, model versioning, and artifact storage.
- **Production Infrastructure**: FastAPI for high-performance serving, PostgreSQL for prediction logging, and Docker for containerization.

## 🏗️ Architecture

![Architecture](https://private-us-east-1.manuscdn.com/sessionFile/hFNVejrrgMRvT3dF7fryn8/sandbox/BiZt1eXAygKDb617chRh4j-images_1780514854755_na1fn_L2hvbWUvdWJ1bnR1L2xsbS1maW5hbmNpYWwtcmlzay1leHBsYWluZXIvYXJjaGl0ZWN0dXJl.png?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9wcml2YXRlLXVzLWVhc3QtMS5tYW51c2Nkbi5jb20vc2Vzc2lvbkZpbGUvaEZOVmVqcnJnTVJ2VDNkRjdmcnluOC9zYW5kYm94L0JpWnQxZVhBeWdLRGI2MTdjaFJoNGotaW1hZ2VzXzE3ODA1MTQ4NTQ3NTVfbmExZm5fTDJodmJXVXZkV0oxYm5SMUwyeHNiUzFtYVc1aGJtTnBZV3d0Y21semF5MWxlSEJzWVdsdVpYSXZZWEpqYUdsMFpXTjBkWEpsLnBuZyIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc5ODc2MTYwMH19fV19&Key-Pair-Id=K2HSFNDJXOU9YS&Signature=Ffp2rNnVx-mKTqxSW5WmtA8WDZmlC-mECNRsRu-UDE0wXhj-JMpgZyHsuL~L-MfJwIlqzMokjMbQ8Lb-n05XBJiyToX-i-8Xb7RosYquaH96NYGZI33dq~TfSyQXjcgULfA6~En6sjQkSgQdVx2SKjZ1hIkMOQdhgXcg-5aewfxG5FGOibCpBito9G2BnAMBILqwBW-RNgEL4Cq0n6Z4TjWL7F7pwoYqsE9Efo15nopzbt-KFJu8mFWBYfKLV1gB~V6fhr7TzMSlidIC2zQ0BWHs7wgaEUD9Y5iZIVOXQQceyUvsmaZNTzCays5Lp1fid9VR~p0qTuUGeTwdntlN~A__)

## 📁 Project Structure

```text

├── app/                    # FastAPI Application
│   ├── api/                # API Endpoints
│   ├── core/               # Database and Config
│   └── services/           # LLM and Business Logic
├── ml/                     # Machine Learning Pipeline
│   ├── data/               # Dataset storage
│   ├── models/             # Saved models and preprocessors
│   └── src/                # Preprocessing, Training, Explanation scripts
├── docker/                 # Dockerfiles
├── tests/                  # Unit and Integration Tests
├── scripts/                # Utility scripts
├── docker-compose.yml      # Multi-container orchestration
└── requirements.txt        # Python dependencies
```

## 🛠️ Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- OpenAI API Key

### Installation & Setup

1. **Clone the repository**
2. **Set up environment variables**:
   Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API Key
   ```
3. **Run the setup script**:
   This will generate sample data, train the model, and start the Docker containers.
   ```bash
   bash scripts/setup.sh
   ```

### Manual Execution (Local)

If you don't want to use Docker:
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Train the model**: `export PYTHONPATH=$PYTHONPATH:$(pwd)/ml/src && python3 ml/src/train.py`
3. **Run the API**: `uvicorn app.api.main:app --reload`

## 📡 API Documentation

Once the API is running, visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Key Endpoints
- `POST /predict`: Predict risk and get LLM explanation.
- `POST /copilot`: Ask questions about a specific prediction.
- `GET /metrics`: Retrieve model performance metrics from MLflow.
- `GET /feature-importance`: Get global feature importance.
- `GET /health`: System health check.

## 🛡️ Compliance & Safety
- **No Hallucinations**: The LLM is strictly grounded in SHAP values and customer data.
- **Compliance-Friendly**: Language is tuned for financial regulatory requirements.
- **Audit Trail**: Every prediction and explanation is logged to PostgreSQL for auditing.

## 🧪 Testing
Run tests using pytest:
```bash
pytest tests/
```

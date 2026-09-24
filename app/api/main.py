
import numpy as np
from fastapi.responses import JSONResponse

def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(i) for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
import joblib
import pandas as pd
import os
import json
from loguru import logger
from sqlalchemy.orm import Session
import mlflow

from app.services.llm_explainer import LLMRiskExplainer
from ml.src.explain import RiskExplainer
from ml.src.preprocess import load_and_preprocess_data
from app.core.database import get_db, PredictionLog, init_db

app = FastAPI(
    title="LLM-Powered Financial Risk Explainer API",
    description="API for predicting loan default risk and generating explainable, compliance-friendly natural language explanations using an LLM.",
    version="1.0.0",
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Load Models and Explainers ---
model = None
preprocessor = None
feature_names = None
risk_explainer = None
llm_explainer = None

@app.on_event("startup")
async def load_resources():
    global model, preprocessor, feature_names, risk_explainer, llm_explainer
    try:
        model_path = "ml/models/best_model.joblib"
        preprocessor_path = "ml/models/preprocessor.joblib"
        
        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)
        
        # Reload data to get feature names after preprocessing
        _, _, _, _, feature_names, _, _ = load_and_preprocess_data("ml/data/loan_data.csv")
        
        risk_explainer = RiskExplainer(model_path, preprocessor_path)
        llm_explainer = LLMRiskExplainer()
        
        # Initialize DB
        init_db()
        
        logger.info("ML Model, Preprocessor, Risk Explainer, LLM Explainer, and DB initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to load resources: {e}")
        # In production, we might want to fail the startup
        # raise HTTPException(status_code=500, detail=f"Failed to load resources: {e}")

# --- Pydantic Models for Request/Response ---
class LoanFeatures(BaseModel):
    age: int
    income: int
    loan_amount: int
    credit_score: int
    employment_years: int
    existing_debts: int
    home_ownership: str
    loan_purpose: str

class PredictionResponse(BaseModel):
    prediction: int
    probability: float
    shap_analysis: Dict[str, Any]
    llm_explanation: Dict[str, Any]

# --- Endpoints ---
@app.get("/health", summary="Health Check", response_model=Dict[str, str])
async def health_check():
    return {"status": "ok"}

@app.get("/model-info", summary="Get Model Information", response_model=Dict[str, str])
async def get_model_info():
    try:
        with open("ml/models/model_info.txt", "r") as f:
            model_info = f.read()
        return {"model_info": model_info}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model information not found.")

@app.post("/predict", summary="Predict Loan Default Risk and Explain", response_model=PredictionResponse)
async def predict_loan_risk(features: LoanFeatures, db: Session = Depends(get_db)):
    if model is None or preprocessor is None or risk_explainer is None or llm_explainer is None:
        raise HTTPException(status_code=503, detail="Model resources not loaded. Please try again later.")

    # Convert input features to DataFrame
    input_df = pd.DataFrame([features.model_dump()])
    
    # Preprocess input
    processed_features = preprocessor.transform(input_df)
    
    # Make prediction
    prediction = int(model.predict(processed_features)[0])
    probability = float(model.predict_proba(processed_features)[:, 1][0])
    
    # Generate SHAP explanations
    shap_explanation = risk_explainer.get_local_explanation(input_df, feature_names)
    
    # Generate LLM explanation
    llm_explanation = llm_explainer.generate_explanation(
        prediction=prediction,
        probability=probability,
        customer_features=features.model_dump(),
        shap_values=shap_explanation
    )
    
    # Log to Database
    try:
        log_entry = PredictionLog(
            input_features=features.model_dump(),
            prediction=prediction,
            probability=probability,
            shap_analysis=shap_explanation,
            llm_explanation=llm_explanation
        )
        db.add(log_entry)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to log prediction to database: {e}")
    
    shap_clean = convert_numpy(shap_explanation) if shap_explanation else {}
    return PredictionResponse(
        prediction=prediction,
        probability=probability,
        shap_analysis=shap_clean,
        llm_explanation=llm_explanation
    )

@app.post("/copilot", summary="Risk Analyst Copilot", response_model=Dict[str, str])
async def risk_analyst_copilot_query(question: str, prediction_data: PredictionResponse):
    if llm_explainer is None:
        raise HTTPException(status_code=503, detail="LLM Explainer not loaded.")
    
    answer = llm_explainer.risk_analyst_copilot(question, prediction_data.model_dump())
    return {"answer": answer}

@app.get("/metrics", summary="Get Model Metrics", response_model=Dict[str, Any])
async def get_model_metrics():
    try:
        with open("ml/models/model_info.txt", "r") as f:
            model_info_lines = f.readlines()
        
        run_id = None
        for line in model_info_lines:
            if "MLflow Run ID:" in line:
                run_id = line.split(":")[-1].strip()
                break
        
        if not run_id:
            raise HTTPException(status_code=404, detail="MLflow Run ID not found in model info.")

        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        metrics = run.data.metrics
        return {"run_id": run_id, "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving MLflow metrics: {e}")

@app.get("/feature-importance", summary="Get Feature Importance", response_model=Dict[str, Any])
async def get_feature_importance():
    try:
        with open("ml/models/model_info.txt", "r") as f:
            model_info_lines = f.readlines()
        
        run_id = None
        for line in model_info_lines:
            if "MLflow Run ID:" in line:
                run_id = line.split(":")[-1].strip()
                break
        
        if not run_id:
            raise HTTPException(status_code=404, detail="MLflow Run ID not found in model info.")

        client = mlflow.tracking.MlflowClient()
        artifact_path = "feature_importance.json"
        local_path = client.download_artifacts(run_id=run_id, path=artifact_path)
        
        with open(local_path, "r") as f:
            feature_importance = json.load(f)
        
        return {"run_id": run_id, "feature_importance": feature_importance}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving feature importance: {e}")

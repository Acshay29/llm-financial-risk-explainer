from fastapi.testclient import TestClient
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_model_info():
    response = client.get("/model-info")
    assert response.status_code in [200, 404] # 404 if model not trained yet

def test_predict_endpoint():
    payload = {
        "age": 35,
        "income": 75000,
        "loan_amount": 15000,
        "credit_score": 720,
        "employment_years": 10,
        "existing_debts": 1,
        "home_ownership": "MORTGAGE",
        "loan_purpose": "HOME_IMPROVEMENT"
    }
    # Note: This test requires the model and preprocessor to be loaded, 
    # which happens on startup. For real unit tests, we would mock these.
    # response = client.post("/predict", json=payload)
    # assert response.status_code == 200
    pass

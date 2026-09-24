import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import joblib
import os
from preprocess import load_and_preprocess_data

def train_and_evaluate():
    # Load data
    data_path = 'ml/data/loan_data.csv'
    X_train, X_test, y_train, y_test, feature_names, X_train_raw, X_test_raw = load_and_preprocess_data(data_path)
    
    # Set MLflow experiment
    mlflow.set_experiment("Loan_Default_Risk_Prediction")
    
    models = {
        "LogisticRegression": LogisticRegression(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "XGBoost": XGBClassifier(n_estimators=100, learning_rate=0.1, random_state=42)
    }
    
    best_model = None
    best_f1 = 0
    best_model_name = ""
    
    for name, model in models.items():
        with mlflow.start_run(run_name=name):
            # Train
            model.fit(X_train, y_train)
            
            # Predict
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            
            # Metrics
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            auc = roc_auc_score(y_test, y_prob)
            
            # Log metrics
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision", prec)
            mlflow.log_metric("recall", rec)
            mlflow.log_metric("f1", f1)
            mlflow.log_metric("roc_auc", auc)
            
            # Log model
            if name == "XGBoost":
                mlflow.xgboost.log_model(model, "model")
            else:
                mlflow.sklearn.log_model(model, "model")

            # Log feature importance for tree-based models
            if hasattr(model, 'feature_importances_'):
                feature_importance_dict = dict(zip(feature_names, model.feature_importances_))
                mlflow.log_dict(feature_importance_dict, "feature_importance.json")
            elif hasattr(model, 'coef_'):
                # For linear models, use coefficients as importance
                feature_importance_dict = dict(zip(feature_names, model.coef_[0]))
                mlflow.log_dict(feature_importance_dict, "feature_importance.json")
            
            print(f"Model: {name}")
            print(f"F1 Score: {f1:.4f}, ROC-AUC: {auc:.4f}")
            
            if f1 > best_f1:
                best_f1 = f1
                best_model = model
                best_model_name = name

    # Save best model
    joblib.dump(best_model, 'ml/models/best_model.joblib')
    with open('ml/models/model_info.txt', 'w') as f:
        f.write(f"Best Model: {best_model_name}\nF1 Score: {best_f1}\nMLflow Run ID: {mlflow.active_run().info.run_id if mlflow.active_run() else 'N/A'}")
    
    print(f"Best model ({best_model_name}) saved.")

if __name__ == "__main__":
    train_and_evaluate()

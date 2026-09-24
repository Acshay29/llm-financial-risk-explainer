import shap
import joblib
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

class RiskExplainer:
    def __init__(self, model_path, preprocessor_path):
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)
        
        # Determine model type for SHAP explainer
        if hasattr(self.model, 'predict_proba'):
            # For Linear models like LogisticRegression, use LinearExplainer
            # For XGBoost/RandomForest, use TreeExplainer
            if 'LogisticRegression' in str(type(self.model)):
                self.explainer_type = 'linear'
            else:
                self.explainer_type = 'tree'
        else:
            self.explainer_type = 'kernel'
            
    def get_local_explanation(self, input_df, feature_names):
        X_processed = self.preprocessor.transform(input_df)
        
        if self.explainer_type == 'linear':
            # LinearExplainer needs background data or just works on coefficients
            explainer = shap.LinearExplainer(self.model, X_processed)
            shap_values = explainer.shap_values(X_processed)
        elif self.explainer_type == 'tree':
            explainer = shap.TreeExplainer(self.model)
            shap_values = explainer.shap_values(X_processed)
        else:
            # Fallback to KernelExplainer (slow)
            explainer = shap.KernelExplainer(self.model.predict_proba, X_processed)
            shap_values = explainer.shap_values(X_processed)

        # For binary classification, shap_values might be a list (one per class)
        # or a single array. We want the values for class 1 (default).
        if isinstance(shap_values, list):
            # For LogisticRegression/RandomForest in older SHAP versions
            sv = shap_values[1] if len(shap_values) > 1 else shap_values[0]
        else:
            # For XGBoost or newer SHAP
            sv = shap_values
            
        # Handle cases where sv is 3D or 2D
        if len(sv.shape) == 2:
            current_sv = sv[0]
        else:
            current_sv = sv

        # Combine features and SHAP values
        explanation = []
        for i, feat in enumerate(feature_names):
            explanation.append({
                "feature": feat,
                "value": input_df.iloc[0].get(feat, "N/A"), # Raw value if available
                "shap_value": float(current_sv[i])
            })
            
        # Sort by absolute SHAP value
        explanation = sorted(explanation, key=lambda x: abs(x['shap_value']), reverse=True)
        
        risk_factors = [e for e in explanation if e['shap_value'] > 0][:5]
        positive_factors = [e for e in explanation if e['shap_value'] < 0][:5]
        
        return {
            "all_features": explanation,
            "risk_factors": risk_factors,
            "positive_factors": positive_factors
        }

if __name__ == "__main__":
    # Test
    from preprocess import load_and_preprocess_data
    data_path = 'ml/data/loan_data.csv'
    _, _, _, _, feature_names, _, X_test_raw = load_and_preprocess_data(data_path)
    
    explainer = RiskExplainer(
        'ml/models/best_model.joblib',
        'ml/models/preprocessor.joblib'
    )
    
    sample_input = X_test_raw.iloc[0:1]
    exp = explainer.get_local_explanation(sample_input, feature_names)
    print("Risk Factors:", exp['risk_factors'])
    print("Positive Factors:", exp['positive_factors'])

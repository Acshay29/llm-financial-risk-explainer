import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import json
import os

def check_drift(reference_data_path, current_data_path, threshold=0.05):
    """
    Check for data drift using Kolmogorov-Smirnov test.
    """
    ref_df = pd.read_csv(reference_data_path)
    cur_df = pd.read_csv(current_data_path)
    
    drift_report = {}
    
    # Check numerical columns
    numerical_cols = ref_df.select_dtypes(exclude=['object']).columns
    
    for col in numerical_cols:
        if col in cur_df.columns:
            stat, p_value = ks_2samp(ref_df[col], cur_df[col])
            is_drifted = p_value < threshold
            drift_report[col] = {
                "p_value": float(p_value),
                "is_drifted": bool(is_drifted)
            }
            
    return drift_report

if __name__ == "__main__":
    # For demonstration, we'll just check the training data against itself
    data_path = 'ml/data/loan_data.csv'
    report = check_drift(data_path, data_path)
    print("Drift Report (Self-Check):")
    print(json.dumps(report, indent=2))

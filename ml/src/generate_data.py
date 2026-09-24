import pandas as pd
import numpy as np
import os

def generate_sample_loan_data(n_samples=1000):
    np.random.seed(42)
    
    data = {
        'age': np.random.randint(18, 70, n_samples),
        'income': np.random.randint(20000, 150000, n_samples),
        'loan_amount': np.random.randint(1000, 50000, n_samples),
        'credit_score': np.random.randint(300, 850, n_samples),
        'employment_years': np.random.randint(0, 40, n_samples),
        'existing_debts': np.random.randint(0, 5, n_samples),
        'home_ownership': np.random.choice(['RENT', 'MORTGAGE', 'OWN'], n_samples),
        'loan_purpose': np.random.choice(['DEBT_CONSOLIDATION', 'HOME_IMPROVEMENT', 'MAJOR_PURCHASE', 'SMALL_BUSINESS'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Simple logic for default risk
    # Higher risk if low credit score, high loan relative to income, or high debts
    risk_score = (
        (850 - df['credit_score']) / 550 * 0.4 +
        (df['loan_amount'] / df['income']) * 0.3 +
        (df['existing_debts'] / 5) * 0.2 +
        (df['age'] < 25).astype(int) * 0.1
    )
    
    df['default'] = (risk_score > 0.5).astype(int)
    
    # Introduce some noise
    noise = np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    df['default'] = np.where(noise == 1, 1 - df['default'], df['default'])
    
    output_path = 'ml/data/loan_data.csv'
    df.to_csv(output_path, index=False)
    print(f"Sample data generated at {output_path}")

if __name__ == "__main__":
    generate_sample_loan_data()

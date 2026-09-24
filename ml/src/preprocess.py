import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

def load_and_preprocess_data(data_path):
    df = pd.read_csv(data_path)
    
    X = df.drop('default', axis=1)
    y = df['default']
    
    # Identify categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(exclude=['object']).columns.tolist()
    
    # Define preprocessing pipelines
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Fit preprocessor
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names after one-hot encoding
    cat_feature_names = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_cols).tolist()
    feature_names = numerical_cols + cat_feature_names
    
    # Save preprocessor
    os.makedirs('ml/models', exist_ok=True)
    joblib.dump(preprocessor, 'ml/models/preprocessor.joblib')
    
    return X_train_processed, X_test_processed, y_train, y_test, feature_names, X_train, X_test

if __name__ == "__main__":
    data_path = 'ml/data/loan_data.csv'
    X_train_p, X_test_p, y_train, y_test, features, X_train_raw, X_test_raw = load_and_preprocess_data(data_path)
    print(f"Data preprocessed. Features: {features}")
    print(f"X_train shape: {X_train_p.shape}")

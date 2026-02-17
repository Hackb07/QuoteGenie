
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error
import pickle
import os
import joblib

# Paths
DATA_PATH = "../data/historical_quotes.csv"
MODEL_DIR = "../backend/models/" # Save directly to backend for inference
WIN_PROB_MODEL_PATH = os.path.join(MODEL_DIR, "win_prob_model.pkl")
PRICE_OPT_MODEL_PATH = os.path.join(MODEL_DIR, "price_opt_model.pkl")
PREPROCESSOR_PATH = os.path.join(MODEL_DIR, "preprocessor.pkl")

# Create model directory
os.makedirs(MODEL_DIR, exist_ok=True)

def train_models():
    print("Loading data...")
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}. Please run generate_data.py first.")
        return

    df = pd.read_csv(DATA_PATH)
    
    # Feature Engineering
    # Define features and target
    categorical_features = ['customer_segment', 'product_category']
    numerical_features = ['weight', 'volume', 'distance', 'fuel_index'] #, 'competitor_rate' (Not available at inference time usually, or maybe it is?)
    # In real world, we might not know competitor rate at quote time, so we should train without it OR predict it.
    # For Win Prob model, we include OUR Quoted Price as a feature.
    
    X = df[categorical_features + numerical_features + ['quoted_price']]
    y_win = df['win']
    y_price = df['market_rate'] if 'market_rate' in df.columns else df['competitor_rate'] # Predict market rate to know baseline

    # Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features + ['quoted_price']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y_win, test_size=0.2, random_state=42)
    
    # --- Model 1: Win Probability (Classification) ---
    print("\nTraining Win Probability Model (XGBoost)...")
    
    # We use a Pipeline to include preprocessing
    win_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb.XGBClassifier(eval_metric='logloss', n_estimators=100))
    ])
    
    win_model.fit(X_train, y_train)
    
    y_pred = win_model.predict(X_test)
    y_prob = win_model.predict_proba(X_test)[:, 1]
    
    print(f"Win Model Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Win Model AUC: {roc_auc_score(y_test, y_prob):.4f}")
    
    # --- Model 2: Price Optimization (Regression - Market Rate Prediction) ---
    # To optimize price, we first need to estimate the market rate to know where to position.
    # We'll use the same features EXCEPT Quoted Price (since we want to predict price independent of our quote).
    
    print("\nTraining Market Rate Estimator (XGBRegressor)...")
    
    # Market rate predictor features (No quoted_price, no win outcome)
    X_market = df[categorical_features + numerical_features]
    y_market = df['competitor_rate'] # approximating market rate with competitor rate
    
    market_preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    price_model = Pipeline(steps=[
        ('preprocessor', market_preprocessor),
        ('regressor', xgb.XGBRegressor(n_estimators=100, objective='reg:squarederror'))
    ])
    
    X_m_train, X_m_test, y_m_train, y_m_test = train_test_split(X_market, y_market, test_size=0.2, random_state=42)
    price_model.fit(X_m_train, y_m_train)
    
    y_m_pred = price_model.predict(X_m_test)
    rmse = np.sqrt(mean_squared_error(y_m_test, y_m_pred))
    print(f"Market Rate RMSE: {rmse:.2f}")

    # Save artifacts
    print("\nSaving models...")
    joblib.dump(win_model, WIN_PROB_MODEL_PATH)
    joblib.dump(price_model, PRICE_OPT_MODEL_PATH) # This effectively serves as our price optimization base
    # Note: We save the pipelines which include preprocessors.
    
    print(f"Models saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_models()

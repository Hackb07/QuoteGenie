import joblib
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Quote Genie API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Models
MODEL_DIR = "models"
WIN_MODEL_PATH = os.path.join(MODEL_DIR, "win_prob_model.pkl")
PRICE_MODEL_PATH = os.path.join(MODEL_DIR, "price_opt_model.pkl")

models = {}

@app.on_event("startup")
def load_models():
    if os.path.exists(WIN_MODEL_PATH) and os.path.exists(PRICE_MODEL_PATH):
        models["win_prob"] = joblib.load(WIN_MODEL_PATH)
        models["price_opt"] = joblib.load(PRICE_MODEL_PATH)
        print("Models loaded successfully.")
    else:
        print("Warning: Models not found. Using fallback/dummy logic.")

class QuoteRequest(BaseModel):
    weight: float
    volume: float
    origin: str
    destination: str
    product_category: str
    customer_segment: str

@app.post("/predict")
def predict_price(request: QuoteRequest):
    # Default fallback logic
    base_rate = 100.0
    recommended_price = base_rate + (request.weight * 0.5) + (request.volume * 100)
    win_probability = 0.75
    confidence_interval = [recommended_price * 0.9, recommended_price * 1.1]
    shap_values = {"weight": request.weight * 0.1, "volume": request.volume * 10}

    # ML Inference Logic
    if "win_prob" in models and "price_opt" in models:
        try:
            # Prepare input dataframe matching training schema
            # Note: In real app, we need to handle distance calculation between origin/destination
            # For this MVP, we estimate distance randomly or fixed
            distance = 500 # Placeholder for calculated distance
            fuel_index = 100.0 # Placeholder
            
            input_df = pd.DataFrame([{
                'customer_segment': request.customer_segment,
                'product_category': request.product_category,
                'weight': request.weight,
                'volume': request.volume,
                'distance': distance,
                'fuel_index': fuel_index
                # 'quoted_price' is needed for win prob model, but not for price opt model
            }])
            
            # Predict Market Rate (Price Optimization Base)
            market_rate_pred = models["price_opt"].predict(input_df)[0]
            
            # Strategy: Recommend price slightly above market rate to maximize margin, 
            # while keeping win prob high.
            # Let's say we target 20% margin over estimated cost (approx market rate - profit)
            # Simplified: Recommend Market Rate
            recommended_price = float(market_rate_pred)
            
            # Predict Win Probability at this price
            # We need to add 'quoted_price' column to input for win model
            input_win = input_df.copy()
            input_win['quoted_price'] = recommended_price
            
            win_probability = float(models["win_prob"].predict_proba(input_win)[0][1])
            
            confidence_interval = [recommended_price * 0.95, recommended_price * 1.05]
            
            # Simplified explainability
            shap_values = {
                "Weight Impact": request.weight * 0.5,
                "Market Cond.": 20.0
            }
            
        except Exception as e:
            print(f"Inference error: {e}")
            # Fallback to default values
            pass
            
    return {
        "recommended_price": recommended_price,
        "win_probability": win_probability,
        "confidence_interval": confidence_interval,
        "shap_values": shap_values
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

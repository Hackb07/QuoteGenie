from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Quote Genie API", version="0.1.0")

class QuoteRequest(BaseModel):
    weight: float
    volume: float
    origin: str
    destination: str
    product_category: str
    customer_segment: str

@app.get("/")
def read_root():
    return {"message": "Welcome to Quote Genie API"}

@app.post("/predict")
def predict_price(request: QuoteRequest):
    # Placeholder implementation
    # In real implementation: 
    # 1. Feature engineer the input
    # 2. Call ML models (Win Prob & Price Opt)
    # 3. Apply business rules
    
    # Example logic
    base_rate = 100.0
    recommended_price = base_rate + (request.weight * 0.5)
    win_probability = 0.85
    
    return {
        "recommended_price": recommended_price,
        "win_probability": win_probability,
        "confidence_interval": [recommended_price * 0.9, recommended_price * 1.1],
        "shap_values": {"weight": 10.5, "origin": 5.0} # Dummy values
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

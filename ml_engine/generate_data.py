import pandas as pd
import numpy as np
import random

# Configuration
NUM_SAMPLES = 5000
OUTPUT_FILE = "../data/historical_quotes.csv"

# Helper functions
def generate_distance(origin, dest):
    # Simplified distance logic
    base_dist = random.randint(100, 3000)
    return base_dist

def calculate_base_cost(weight, volume, distance, fuel_index):
    # Cost model: Base + (Weight * Rate) + Volumetric + Distance + Fuel
    weight_cost = weight * 0.5
    vol_cost = volume * 100
    dist_cost = distance * 0.8
    fuel_surcharge = fuel_index * 1.2
    return 50 + weight_cost + vol_cost + dist_cost + fuel_surcharge

def determine_win(price, market_rate, sensitivity):
    # Logistic function for win probability based on price vs market
    diff = (market_rate - price) / market_rate
    # Sensitivity acts as a multiplier
    prob = 1 / (1 + np.exp(-10 * (diff + (0.1 * (1 - sensitivity)))))
    return np.random.random() < prob

# Data Generation
print(f"Generating {NUM_SAMPLES} historical quotes...")

data = {
    'quote_id': range(1, NUM_SAMPLES + 1),
    'customer_segment': np.random.choice(['Standard', 'Premium', 'Strategic'], NUM_SAMPLES, p=[0.6, 0.3, 0.1]),
    'product_category': np.random.choice(['General', 'Electronics', 'Perishable', 'Hazardous'], NUM_SAMPLES, p=[0.5, 0.2, 0.2, 0.1]),
    'weight': np.random.lognormal(mean=4, sigma=1, size=NUM_SAMPLES), # Skewed weight distribution
    'volume': np.random.lognormal(mean=0, sigma=0.5, size=NUM_SAMPLES),
    'distance': np.random.uniform(50, 5000, NUM_SAMPLES),
    'fuel_index': np.random.uniform(90, 120, NUM_SAMPLES),
    'competitor_rate': [], # Will be calculated
    'quoted_price': [],
    'cost': [],
    'win': []
}

# Post-processing logic
for i in range(NUM_SAMPLES):
    # Adjust sensitivity based on segment
    sensitivity = {
        'Standard': 0.8,
        'Premium': 0.5,
        'Strategic': 0.3 # Less sensitive due to long-term contracts
    }[data['customer_segment'][i]]
    
    # Calculate costs
    cost = calculate_base_cost(
        data['weight'][i], 
        data['volume'][i], 
        data['distance'][i], 
        data['fuel_index'][i]
    )
    
    # Simulate market 
    market_rate = cost * np.random.uniform(1.1, 1.4) 
    
    # Quote simulation: Reps quote around market rate + variance
    quoted_price = market_rate * np.random.uniform(0.9, 1.2)
    
    # Outcome
    is_win = determine_win(quoted_price, market_rate, sensitivity)
    
    data['competitor_rate'].append(market_rate)
    data['quoted_price'].append(quoted_price)
    data['cost'].append(cost)
    data['win'].append(1 if is_win else 0)

df = pd.DataFrame(data)

# Save
df.to_csv(OUTPUT_FILE, index=False)
print(f"Data saved to {OUTPUT_FILE}")
print(df.head())

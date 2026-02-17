-- Quote Genie Database Schema

CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    segment VARCHAR(50), -- 'standard', 'premium', 'strategic'
    price_sensitivity_score FLOAT
);

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    origin_city VARCHAR(100),
    origin_country VARCHAR(100),
    dest_city VARCHAR(100),
    dest_country VARCHAR(100),
    weight_kg FLOAT,
    volume_m3 FLOAT,
    product_category VARCHAR(50), -- 'general', 'electronics', 'perishable', 'hazardous'
    distance_km FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quotes (
    quote_id SERIAL PRIMARY KEY,
    shipment_id INT REFERENCES shipments(shipment_id),
    quoted_price DECIMAL(10, 2),
    cost_base DECIMAL(10, 2),
    margin_percent DECIMAL(5, 2),
    win_probability_predicted FLOAT,
    outcome BOOLEAN, -- TRUE = Won, FALSE = Lost
    feedback_notes TEXT
);

-- Market Data Table
CREATE TABLE IF NOT EXISTS market_indices (
    date DATE PRIMARY KEY,
    fuel_index DECIMAL(10, 2),
    demand_index DECIMAL(10, 2)
);

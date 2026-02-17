import React, { useState } from 'react';
import { getQuote } from '../api/quoteApi';
import { Package, Truck, ArrowRight, DollarSign, TrendingUp, AlertCircle, Loader } from 'lucide-react';

const QuoteForm = () => {
    const [formData, setFormData] = useState({
        weight: '',
        volume: '',
        origin: '',
        destination: '',
        product_category: 'general',
        customer_segment: 'standard'
    });

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        try {
            const data = await getQuote({
                ...formData,
                weight: parseFloat(formData.weight),
                volume: parseFloat(formData.volume)
            });
            setResult(data);
        } catch (err) {
            setError('Failed to fetch quote. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="quote-container">
            <div className="glass-panel form-panel">
                <h2 className="panel-title"><Package size={24} /> Get Shipment Quote</h2>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Weight (kg)</label>
                        <input
                            type="number"
                            name="weight"
                            placeholder="e.g. 150"
                            value={formData.weight}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Volume (m³)</label>
                        <input
                            type="number"
                            name="volume"
                            placeholder="e.g. 0.5"
                            value={formData.volume}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Origin</label>
                        <input
                            type="text"
                            name="origin"
                            placeholder="City, Country"
                            value={formData.origin}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Destination</label>
                        <input
                            type="text"
                            name="destination"
                            placeholder="City, Country"
                            value={formData.destination}
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <div className="form-row">
                        <div className="form-group">
                            <label>Product Category</label>
                            <select name="product_category" value={formData.product_category} onChange={handleChange}>
                                <option value="general">General</option>
                                <option value="electronics">Electronics</option>
                                <option value="perishable">Perishable</option>
                                <option value="hazardous">Hazardous</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Customer Segment</label>
                            <select name="customer_segment" value={formData.customer_segment} onChange={handleChange}>
                                <option value="standard">Standard</option>
                                <option value="premium">Premium</option>
                                <option value="strategic">Strategic</option>
                            </select>
                        </div>
                    </div>

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? <Loader className="spin" size={20} /> : <><Truck size={20} /> Calculate Quote</>}
                    </button>

                    {error && <div className="error-msg"><AlertCircle size={16} /> {error}</div>}
                </form>
            </div>

            {result && (
                <div className="glass-panel result-panel fade-in">
                    <h2 className="panel-title"><TrendingUp size={24} /> Quote Analysis</h2>

                    <div className="metric-card recommended-price">
                        <span className="metric-label">Recommended Price</span>
                        <div className="metric-value">
                            <DollarSign size={28} />
                            {result.recommended_price.toFixed(2)}
                        </div>
                        <div className="metric-sub">
                            Range: ${result.confidence_interval[0].toFixed(2)} - ${result.confidence_interval[1].toFixed(2)}
                        </div>
                    </div>

                    <div className="metric-card win-prob">
                        <span className="metric-label">Win Probability</span>
                        <div className="metric-value">
                            {(result.win_probability * 100).toFixed(1)}%
                        </div>
                        <div className="progress-bar">
                            <div
                                className="progress-fill"
                                style={{ width: `${result.win_probability * 100}%` }}
                            ></div>
                        </div>
                    </div>

                    <div className="factors-list">
                        <h3>Key Influencing Factors</h3>
                        <ul>
                            {Object.entries(result.shap_values).map(([key, value]) => (
                                <li key={key}>
                                    <span className="factor-name">{key}</span>
                                    <span className={`factor-impact ${value > 0 ? 'positive' : 'negative'}`}>
                                        {value > 0 ? '+' : ''}{value.toFixed(1)}
                                    </span>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            )}
        </div>
    );
};

export default QuoteForm;

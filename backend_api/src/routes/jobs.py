from flask import Blueprint, jsonify, request
import pandas as pd
import pickle
import numpy as np
from datetime import datetime
import os

jobs_bp = Blueprint('jobs', __name__)

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'india_jobs_data.csv')
MODELS_PATH = os.path.join(os.path.dirname(__file__), '..', 'models')

def load_data():
    return pd.read_csv(DATA_PATH)

def load_linear_regression_model():
    with open(os.path.join(MODELS_PATH, 'linear_regression_model.pkl'), 'rb') as f:
        return pickle.load(f)

def load_prophet_models():
    with open(os.path.join(MODELS_PATH, 'prophet_models.pkl'), 'rb') as f:
        return pickle.load(f)

@jobs_bp.route('/sectors', methods=['GET'])
def get_sectors():
    """Get all available sectors"""
    try:
        df = load_data()
        sectors = df['Sector'].unique().tolist()
        return jsonify({'sectors': sectors})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/years', methods=['GET'])
def get_years():
    """Get all available years"""
    try:
        df = load_data()
        years = sorted(df['Year'].unique().tolist())
        return jsonify({'years': years})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/data', methods=['GET'])
def get_data():
    """Get employment data for a specific sector and year"""
    try:
        sector = request.args.get('sector')
        year = request.args.get('year', type=int)
        
        df = load_data()
        
        if sector and year:
            filtered_df = df[(df['Sector'] == sector) & (df['Year'] == year)]
        elif sector:
            filtered_df = df[df['Sector'] == sector]
        elif year:
            filtered_df = df[df['Year'] == year]
        else:
            filtered_df = df
        
        return jsonify(filtered_df.to_dict('records'))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/trends', methods=['GET'])
def get_trends():
    """Get trend data for a specific sector"""
    try:
        sector = request.args.get('sector')
        if not sector:
            return jsonify({'error': 'Sector parameter is required'}), 400
        
        df = load_data()
        sector_df = df[df['Sector'] == sector].sort_values('Year')
        
        trends = {
            'years': sector_df['Year'].tolist(),
            'estimated_jobs': sector_df['Estimated_Jobs'].tolist(),
            'actual_jobs': sector_df['Actual_Jobs'].tolist(),
            'installed_capacity': sector_df['Installed_Capacity_MW'].tolist()
        }
        
        return jsonify(trends)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/predict', methods=['POST'])
def predict_jobs():
    """Predict future job numbers using ML models"""
    try:
        data = request.get_json()
        sector = data.get('sector')
        year = data.get('year')
        installed_capacity = data.get('installed_capacity', 0)
        model_type = data.get('model_type', 'linear_regression')
        
        if not sector or not year:
            return jsonify({'error': 'Sector and year are required'}), 400
        
        df = load_data()
        
        if model_type == 'linear_regression':
            # Load linear regression model
            model = load_linear_regression_model()
            
            # Prepare input data
            df_encoded = pd.get_dummies(df, columns=['Sector'], drop_first=True)
            feature_columns = ['Year', 'Installed_Capacity_MW'] + [col for col in df_encoded.columns if 'Sector_' in col]
            
            # Create input vector
            input_data = pd.DataFrame({
                'Year': [year],
                'Installed_Capacity_MW': [installed_capacity]
            })
            
            # Add sector dummy variables
            for col in feature_columns:
                if col.startswith('Sector_'):
                    sector_name = col.replace('Sector_', '')
                    input_data[col] = [1 if sector == sector_name else 0]
                elif col not in input_data.columns:
                    input_data[col] = [0]
            
            # Ensure columns are in the same order as training
            input_data = input_data[feature_columns]
            
            prediction = model.predict(input_data)[0]
            
        elif model_type == 'prophet':
            # Load Prophet models
            prophet_models = load_prophet_models()
            
            if sector not in prophet_models:
                return jsonify({'error': f'Prophet model not available for sector: {sector}'}), 400
            
            model = prophet_models[sector]
            
            # Create future dataframe
            future_df = pd.DataFrame({
                'ds': [pd.to_datetime(f'{year}-12-31')],
                'Installed_Capacity_MW': [installed_capacity]
            })
            
            forecast = model.predict(future_df)
            prediction = forecast['yhat'].iloc[0]
            
        else:
            return jsonify({'error': 'Invalid model type'}), 400
        
        # Calculate growth rate if possible
        historical_data = df[df['Sector'] == sector].sort_values('Year')
        if len(historical_data) > 0:
            last_year_jobs = historical_data['Actual_Jobs'].iloc[-1]
            growth_rate = ((prediction - last_year_jobs) / last_year_jobs) * 100
        else:
            growth_rate = 0
        
        return jsonify({
            'sector': sector,
            'year': year,
            'predicted_jobs': int(prediction),
            'model_type': model_type,
            'growth_rate': round(growth_rate, 2),
            'installed_capacity': installed_capacity
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/insights', methods=['GET'])
def get_insights():
    """Get insights and statistics for a specific sector"""
    try:
        sector = request.args.get('sector')
        if not sector:
            return jsonify({'error': 'Sector parameter is required'}), 400
        
        df = load_data()
        sector_df = df[df['Sector'] == sector].sort_values('Year')
        
        if len(sector_df) == 0:
            return jsonify({'error': 'No data found for the specified sector'}), 404
        
        # Calculate insights
        total_growth = ((sector_df['Actual_Jobs'].iloc[-1] - sector_df['Actual_Jobs'].iloc[0]) / sector_df['Actual_Jobs'].iloc[0]) * 100
        avg_deviation = np.mean(np.abs(sector_df['Estimated_Jobs'] - sector_df['Actual_Jobs']) / sector_df['Estimated_Jobs'] * 100)
        capacity_correlation = np.corrcoef(sector_df['Installed_Capacity_MW'], sector_df['Actual_Jobs'])[0, 1]
        
        insights = {
            'sector': sector,
            'total_growth_percentage': round(total_growth, 2),
            'average_estimation_deviation': round(avg_deviation, 2),
            'capacity_job_correlation': round(capacity_correlation, 3),
            'years_of_data': len(sector_df),
            'latest_year': int(sector_df['Year'].max()),
            'latest_jobs': int(sector_df['Actual_Jobs'].iloc[-1]),
            'latest_capacity': int(sector_df['Installed_Capacity_MW'].iloc[-1])
        }
        
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


import os
import csv
from flask import Flask, send_from_directory, request
from flask_cors import CORS
import sys

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))

from mw_job_predictor import predict_jobs_from_mw

# Load data from CSV using csv module
def load_data(data_path):
    data = {
        "sectors": [],
        "years": [],
        "data": {}
    }
    
    with open(data_path, mode='r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        
        all_sectors = set()
        all_years = set()
        
        for row in rows:
            sector = row["Sector"]
            year = int(row["Year"])
            # Remove commas before converting to int
            estimated_jobs = int(row["Estimated_Jobs"].replace(",", ""))
            actual_jobs = int(row["Actual_Jobs"].replace(",", ""))
            # Convert to float first, then int if needed, or keep as float
            installed_capacity = float(row["Installed_Capacity_MW"].replace(",", ""))
            
            all_sectors.add(sector)
            all_years.add(year)
            
            if sector not in data["data"]:
                data["data"][sector] = {
                    "years": [],
                    "estimated_jobs": [],
                    "actual_jobs": [],
                    "installed_capacity": []
                }
            
            data["data"][sector]["years"].append(year)
            data["data"][sector]["estimated_jobs"].append(estimated_jobs)
            data["data"][sector]["actual_jobs"].append(actual_jobs)
            data["data"][sector]["installed_capacity"].append(installed_capacity)
            
    data["sectors"] = sorted(list(all_sectors))
    data["years"] = sorted(list(all_years))
    
    # Sort data within each sector by year
    for sector_name in data["data"]:
        sector_entry = data["data"][sector_name]
        sorted_indices = sorted(range(len(sector_entry["years"])), key=lambda k: sector_entry["years"][k])
        sector_entry["years"] = [sector_entry["years"][i] for i in sorted_indices]
        sector_entry["estimated_jobs"] = [sector_entry["estimated_jobs"][i] for i in sorted_indices]
        sector_entry["actual_jobs"] = [sector_entry["actual_jobs"][i] for i in sorted_indices]
        sector_entry["installed_capacity"] = [sector_entry["installed_capacity"][i] for i in sorted_indices]

    return data

data_path = os.path.join(os.path.dirname(__file__), 'data', 'jobs_data.csv')
SAMPLE_DATA = load_data(data_path)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

@app.route('/api/jobs/sectors')
def get_sectors():
    return {'sectors': SAMPLE_DATA['sectors']}

@app.route('/api/jobs/years')
def get_years():
    return {'years': SAMPLE_DATA['years']}

@app.route('/api/jobs/trends')
def get_trends():
    sector = request.args.get('sector')
    if sector and sector in SAMPLE_DATA['data']:
        return SAMPLE_DATA['data'][sector]
    return {'error': 'Sector not found'}, 404

@app.route('/api/jobs/insights')
def get_insights():
    sector = request.args.get('sector')
    if sector and sector in SAMPLE_DATA['data']:
        sector_data = SAMPLE_DATA['data'][sector]
        estimated_jobs = sector_data['estimated_jobs']
        actual_jobs = sector_data['actual_jobs']
        years = sector_data['years']

        total_growth_percentage = ((actual_jobs[-1] - actual_jobs[0]) / actual_jobs[0]) * 100 if actual_jobs[0] != 0 else 0
        
        # Calculate accuracy as percentage of correct predictions (inverse of error rate)
        # Use Mean Absolute Percentage Error (MAPE) for better accuracy representation
        mape = sum([abs((e - a) / a) * 100 for e, a in zip(estimated_jobs, actual_jobs) if a != 0]) / len([a for a in actual_jobs if a != 0]) if actual_jobs else 0
        accuracy_percentage = max(0, 100 - mape)  # Ensure accuracy doesn't go negative
        
        # Also calculate average absolute deviation for reference
        average_estimation_deviation = sum([abs(e - a) for e, a in zip(estimated_jobs, actual_jobs)]) / len(estimated_jobs) if estimated_jobs else 0

        return {
            'total_growth_percentage': round(total_growth_percentage, 2),
            'latest_jobs': actual_jobs[-1],
            'latest_capacity': sector_data['installed_capacity'][-1],
            'average_estimation_deviation': round(average_estimation_deviation, 2),
            'accuracy_percentage': round(accuracy_percentage, 2),
            'years_of_data': len(years),
            'latest_year': years[-1]
        }
    return {'error': 'Sector not found'}, 404

@app.route('/api/jobs/predict', methods=['POST'])
def predict_jobs():
    data = request.json
    sector = data.get('sector')
    year = data.get('year')

    if sector not in SAMPLE_DATA['data']:
        return {'error': 'Sector not found'}, 404

    sector_data = SAMPLE_DATA['data'][sector]
    latest_year = max(sector_data['years'])
    latest_actual_jobs = sector_data['actual_jobs'][sector_data['years'].index(latest_year)]

    # Simple linear extrapolation for prediction
    # This is a placeholder, a real ML model would be more complex
    if latest_year < year:
        # Calculate growth rate based on the last two data points for a more recent trend
        if len(sector_data['actual_jobs']) >= 2:
            prev_year_jobs = sector_data['actual_jobs'][-2]
            if prev_year_jobs != 0:
                growth_rate_per_year = (latest_actual_jobs - prev_year_jobs) / prev_year_jobs
            else:
                growth_rate_per_year = 0
        else:
            growth_rate_per_year = 0 # Fallback if not enough data points

        predicted_jobs = latest_actual_jobs * (1 + growth_rate_per_year * (year - latest_year))
    else:
        predicted_jobs = latest_actual_jobs # If predicting for a past or current year, return latest actual

    return {
        'sector': sector,
        'year': year,
        'predicted_jobs': int(predicted_jobs),
        'growth_rate': round(growth_rate_per_year * 100, 2),
        'model_type': 'linear_extrapolation'
    }

@app.route('/api/jobs/predict-mw', methods=['POST'])
def predict_jobs_by_mw():
    """
    Predict jobs based on MW capacity for a given sector
    """
    data = request.json
    sector = data.get('sector')
    mw_capacity = data.get('mw_capacity')

    if not sector or mw_capacity is None:
        return {'error': 'Sector and MW capacity are required'}, 400

    if sector not in SAMPLE_DATA['sectors']:
        return {'error': 'Sector not found'}, 404

    try:
        predicted_jobs = predict_jobs_from_mw(mw_capacity, sector)
        
        if predicted_jobs is None:
            return {'error': 'Unable to predict jobs for this sector'}, 500

        return {
            'sector': sector,
            'mw_capacity': mw_capacity,
            'predicted_jobs': predicted_jobs,
            'model_type': 'linear_regression_mw'
        }
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}, 500

@app.route('/', defaults={'path': ''}) 
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



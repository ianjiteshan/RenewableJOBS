import os
import csv
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Embedded data - using the exact data from the CSV file
EMBEDDED_DATA = [
    {"Year": "2013", "Sector": "Solar", "Estimated_Jobs": "40000", "Actual_Jobs": "38,000", "Installed_Capacity_MW": "2821.91"},
    {"Year": "2013", "Sector": "Wind", "Estimated_Jobs": "3000", "Actual_Jobs": "25,555", "Installed_Capacity_MW": "21042.58"},
    {"Year": "2013", "Sector": "Biomass", "Estimated_Jobs": "14000", "Actual_Jobs": "13,000", "Installed_Capacity_MW": "7951.05"},
    {"Year": "2013", "Sector": "Hydroelectric", "Estimated_Jobs": "25000", "Actual_Jobs": "23,000", "Installed_Capacity_MW": "3803.68"},
    {"Year": "2013", "Sector": "Geothermal", "Estimated_Jobs": "7500", "Actual_Jobs": "6000", "Installed_Capacity_MW": "400"},
    {"Year": "2014", "Sector": "Solar", "Estimated_Jobs": "50000", "Actual_Jobs": "42000", "Installed_Capacity_MW": "3993.53"},
    {"Year": "2014", "Sector": "Wind", "Estimated_Jobs": "35000", "Actual_Jobs": "31000", "Installed_Capacity_MW": "23354.35"},
    {"Year": "2014", "Sector": "Biomass", "Estimated_Jobs": "15000", "Actual_Jobs": "13500", "Installed_Capacity_MW": "8306.77"},
    {"Year": "2014", "Sector": "Hydroelectric", "Estimated_Jobs": "25000", "Actual_Jobs": "23000", "Installed_Capacity_MW": "4055.36"},
    {"Year": "2014", "Sector": "Geothermal", "Estimated_Jobs": "8000", "Actual_Jobs": "7200", "Installed_Capacity_MW": "400"},
    {"Year": "2015", "Sector": "Solar", "Estimated_Jobs": "70000", "Actual_Jobs": "64000", "Installed_Capacity_MW": "7123.89"},
    {"Year": "2015", "Sector": "Wind", "Estimated_Jobs": "40000", "Actual_Jobs": "36000", "Installed_Capacity_MW": "28700.44"},
    {"Year": "2015", "Sector": "Biomass", "Estimated_Jobs": "16000", "Actual_Jobs": "14000", "Installed_Capacity_MW": "8662.49"},
    {"Year": "2015", "Sector": "Hydroelectric", "Estimated_Jobs": "26000", "Actual_Jobs": "24000", "Installed_Capacity_MW": "4307.04"},
    {"Year": "2015", "Sector": "Geothermal", "Estimated_Jobs": "8500", "Actual_Jobs": "7800", "Installed_Capacity_MW": "400"},
    {"Year": "2016", "Sector": "Solar", "Estimated_Jobs": "85000", "Actual_Jobs": "78000", "Installed_Capacity_MW": "12782.52"},
    {"Year": "2016", "Sector": "Wind", "Estimated_Jobs": "45000", "Actual_Jobs": "41000", "Installed_Capacity_MW": "32280.13"},
    {"Year": "2016", "Sector": "Biomass", "Estimated_Jobs": "17000", "Actual_Jobs": "15000", "Installed_Capacity_MW": "9018.21"},
    {"Year": "2016", "Sector": "Hydroelectric", "Estimated_Jobs": "27000", "Actual_Jobs": "25000", "Installed_Capacity_MW": "4558.72"},
    {"Year": "2016", "Sector": "Geothermal", "Estimated_Jobs": "9000", "Actual_Jobs": "8500", "Installed_Capacity_MW": "400"},
    {"Year": "2017", "Sector": "Solar", "Estimated_Jobs": "120000", "Actual_Jobs": "110000", "Installed_Capacity_MW": "18327.37"},
    {"Year": "2017", "Sector": "Wind", "Estimated_Jobs": "50000", "Actual_Jobs": "46000", "Installed_Capacity_MW": "32848.14"},
    {"Year": "2017", "Sector": "Biomass", "Estimated_Jobs": "18000", "Actual_Jobs": "16000", "Installed_Capacity_MW": "9373.93"},
    {"Year": "2017", "Sector": "Hydroelectric", "Estimated_Jobs": "28000", "Actual_Jobs": "26000", "Installed_Capacity_MW": "4810.4"},
    {"Year": "2017", "Sector": "Geothermal", "Estimated_Jobs": "9500", "Actual_Jobs": "9000", "Installed_Capacity_MW": "400"},
    {"Year": "2018", "Sector": "Solar", "Estimated_Jobs": "150000", "Actual_Jobs": "140000", "Installed_Capacity_MW": "28180.79"},
    {"Year": "2018", "Sector": "Wind", "Estimated_Jobs": "55000", "Actual_Jobs": "51000", "Installed_Capacity_MW": "35129.9"},
    {"Year": "2018", "Sector": "Biomass", "Estimated_Jobs": "19000", "Actual_Jobs": "17000", "Installed_Capacity_MW": "9729.65"},
    {"Year": "2018", "Sector": "Hydroelectric", "Estimated_Jobs": "29000", "Actual_Jobs": "27000", "Installed_Capacity_MW": "5062.08"},
    {"Year": "2018", "Sector": "Geothermal", "Estimated_Jobs": "10000", "Actual_Jobs": "9500", "Installed_Capacity_MW": "400"},
    {"Year": "2019", "Sector": "Solar", "Estimated_Jobs": "180000", "Actual_Jobs": "170000", "Installed_Capacity_MW": "39874.63"},
    {"Year": "2019", "Sector": "Wind", "Estimated_Jobs": "60000", "Actual_Jobs": "56000", "Installed_Capacity_MW": "62025.1"},
    {"Year": "2019", "Sector": "Biomass", "Estimated_Jobs": "20000", "Actual_Jobs": "18000", "Installed_Capacity_MW": "10085.37"},
    {"Year": "2019", "Sector": "Hydroelectric", "Estimated_Jobs": "30000", "Actual_Jobs": "28000", "Installed_Capacity_MW": "5313.76"},
    {"Year": "2019", "Sector": "Geothermal", "Estimated_Jobs": "10500", "Actual_Jobs": "10000", "Installed_Capacity_MW": "400"},
    {"Year": "2020", "Sector": "Solar", "Estimated_Jobs": "200000", "Actual_Jobs": "190000", "Installed_Capacity_MW": "39247.77"},
    {"Year": "2020", "Sector": "Wind", "Estimated_Jobs": "65000", "Actual_Jobs": "61000", "Installed_Capacity_MW": "59503.69"},
    {"Year": "2020", "Sector": "Biomass", "Estimated_Jobs": "21000", "Actual_Jobs": "19000", "Installed_Capacity_MW": "10441.09"},
    {"Year": "2020", "Sector": "Hydroelectric", "Estimated_Jobs": "31000", "Actual_Jobs": "29000", "Installed_Capacity_MW": "5565.44"},
    {"Year": "2020", "Sector": "Geothermal", "Estimated_Jobs": "11000", "Actual_Jobs": "10500", "Installed_Capacity_MW": "400"},
    {"Year": "2021", "Sector": "Solar", "Estimated_Jobs": "220000", "Actual_Jobs": "210000", "Installed_Capacity_MW": "48556.02"},
    {"Year": "2021", "Sector": "Wind", "Estimated_Jobs": "70000", "Actual_Jobs": "66000", "Installed_Capacity_MW": "64077.7"},
    {"Year": "2021", "Sector": "Biomass", "Estimated_Jobs": "22000", "Actual_Jobs": "20000", "Installed_Capacity_MW": "10796.81"},
    {"Year": "2021", "Sector": "Hydroelectric", "Estimated_Jobs": "32000", "Actual_Jobs": "30000", "Installed_Capacity_MW": "5817.12"},
    {"Year": "2021", "Sector": "Geothermal", "Estimated_Jobs": "11500", "Actual_Jobs": "11000", "Installed_Capacity_MW": "400"},
    {"Year": "2022", "Sector": "Solar", "Estimated_Jobs": "250000", "Actual_Jobs": "240000", "Installed_Capacity_MW": "62400.24"},
    {"Year": "2022", "Sector": "Wind", "Estimated_Jobs": "75000", "Actual_Jobs": "71000", "Installed_Capacity_MW": "70307.8"},
    {"Year": "2022", "Sector": "Biomass", "Estimated_Jobs": "23000", "Actual_Jobs": "21000", "Installed_Capacity_MW": "11152.53"},
    {"Year": "2022", "Sector": "Hydroelectric", "Estimated_Jobs": "33000", "Actual_Jobs": "31000", "Installed_Capacity_MW": "6068.8"},
    {"Year": "2022", "Sector": "Geothermal", "Estimated_Jobs": "12000", "Actual_Jobs": "11500", "Installed_Capacity_MW": "400"},
    {"Year": "2023", "Sector": "Solar", "Estimated_Jobs": "280000", "Actual_Jobs": "270000", "Installed_Capacity_MW": "73310.46"},
    {"Year": "2023", "Sector": "Wind", "Estimated_Jobs": "80000", "Actual_Jobs": "76000", "Installed_Capacity_MW": "75032.32"},
    {"Year": "2023", "Sector": "Biomass", "Estimated_Jobs": "24000", "Actual_Jobs": "22000", "Installed_Capacity_MW": "11508.25"},
    {"Year": "2023", "Sector": "Hydroelectric", "Estimated_Jobs": "34000", "Actual_Jobs": "32000", "Installed_Capacity_MW": "6320.48"},
    {"Year": "2023", "Sector": "Geothermal", "Estimated_Jobs": "12500", "Actual_Jobs": "12000", "Installed_Capacity_MW": "400"}
]

# Global data storage
SAMPLE_DATA = None

def load_data():
    """Load data from embedded data"""
    global SAMPLE_DATA
    
    data = {
        "sectors": [],
        "years": [],
        "data": {},
        "raw_data": EMBEDDED_DATA
    }
    
    try:
        all_sectors = set()
        all_years = set()
        
        for row in EMBEDDED_DATA:
            sector = row["Sector"]
            year = int(row["Year"])
            
            # Clean the data
            estimated_jobs = int(str(row["Estimated_Jobs"]).replace(",", "").replace('"', ''))
            actual_jobs = int(str(row["Actual_Jobs"]).replace(",", "").replace('"', ''))
            installed_capacity = float(row["Installed_Capacity_MW"])
            
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

        SAMPLE_DATA = data
        print(f"Data loaded successfully: {len(EMBEDDED_DATA)} records, {len(data['sectors'])} sectors")
        return True
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return False

def predict_jobs_from_mw(mw_capacity, sector):
    """Simple MW-based job prediction"""
    if not SAMPLE_DATA:
        return None
        
    sector_data = [row for row in SAMPLE_DATA["raw_data"] if row['Sector'] == sector]
    if not sector_data:
        return None
    
    # Calculate average jobs per MW
    total_jobs = 0
    total_mw = 0
    
    for row in sector_data:
        actual_jobs = int(str(row['Actual_Jobs']).replace(',', '').replace('"', ''))
        mw = float(row['Installed_Capacity_MW'])
        total_jobs += actual_jobs
        total_mw += mw
    
    if total_mw == 0:
        return None
    
    jobs_per_mw = total_jobs / total_mw
    predicted_jobs = int(mw_capacity * jobs_per_mw)
    
    return max(0, predicted_jobs)

@app.route('/')
def health_check():
    return {'status': 'healthy', 'message': 'Renewable Energy Jobs API', 'data_loaded': SAMPLE_DATA is not None}

@app.route('/api/jobs/sectors')
def get_sectors():
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
    return {'sectors': SAMPLE_DATA['sectors']}

@app.route('/api/jobs/years')
def get_years():
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
    return {'years': SAMPLE_DATA['years']}

@app.route('/api/jobs/trends')
def get_trends():
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
        
    sector = request.args.get('sector')
    if sector and sector in SAMPLE_DATA['data']:
        return SAMPLE_DATA['data'][sector]
    return {'error': 'Sector not found'}, 404

@app.route('/api/jobs/insights')
def get_insights():
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
        
    sector = request.args.get('sector')
    if sector and sector in SAMPLE_DATA['data']:
        sector_data = SAMPLE_DATA['data'][sector]
        estimated_jobs = sector_data['estimated_jobs']
        actual_jobs = sector_data['actual_jobs']
        years = sector_data['years']

        if not actual_jobs or len(actual_jobs) == 0:
            return {'error': 'No data available for sector'}, 404

        total_growth_percentage = ((actual_jobs[-1] - actual_jobs[0]) / actual_jobs[0]) * 100 if actual_jobs[0] != 0 else 0
        average_estimation_deviation = sum([abs(e - a) for e, a in zip(estimated_jobs, actual_jobs)]) / len(estimated_jobs) if estimated_jobs else 0

        return {
            'total_growth_percentage': round(total_growth_percentage, 2),
            'latest_jobs': actual_jobs[-1],
            'latest_capacity': sector_data['installed_capacity'][-1],
            'average_estimation_deviation': round(average_estimation_deviation, 2),
            'years_of_data': len(years),
            'latest_year': years[-1]
        }
    return {'error': 'Sector not found'}, 404

@app.route('/api/jobs/predict', methods=['POST'])
def predict_jobs():
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
        
    data = request.json
    sector = data.get('sector')
    year = data.get('year')

    if sector not in SAMPLE_DATA['data']:
        return {'error': 'Sector not found'}, 404

    sector_data = SAMPLE_DATA['data'][sector]
    latest_year = max(sector_data['years'])
    latest_actual_jobs = sector_data['actual_jobs'][sector_data['years'].index(latest_year)]

    # Simple linear extrapolation for prediction
    if latest_year < year:
        if len(sector_data['actual_jobs']) >= 2:
            prev_year_jobs = sector_data['actual_jobs'][-2]
            if prev_year_jobs != 0:
                growth_rate_per_year = (latest_actual_jobs - prev_year_jobs) / prev_year_jobs
            else:
                growth_rate_per_year = 0
        else:
            growth_rate_per_year = 0

        predicted_jobs = latest_actual_jobs * (1 + growth_rate_per_year * (year - latest_year))
    else:
        predicted_jobs = latest_actual_jobs

    return {
        'sector': sector,
        'year': year,
        'predicted_jobs': int(predicted_jobs),
        'growth_rate': round(growth_rate_per_year * 100, 2) if 'growth_rate_per_year' in locals() else 0,
        'model_type': 'linear_extrapolation'
    }

@app.route('/api/jobs/predict-mw', methods=['POST'])
def predict_jobs_by_mw():
    """Predict jobs based on MW capacity for a given sector"""
    if not SAMPLE_DATA:
        return {'error': 'Data not loaded'}, 500
        
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
            'model_type': 'simple_linear_mw'
        }
    except Exception as e:
        return {'error': f'Prediction failed: {str(e)}'}, 500

if __name__ == '__main__':
    print("Starting Renewable Energy Jobs API...")
    if load_data():
        print("Data loaded successfully!")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("Failed to load data. Exiting.")


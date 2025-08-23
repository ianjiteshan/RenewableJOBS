import os
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from data_preprocessor import preprocess_data

def train_mw_predictor(data_path):
    df = preprocess_data(data_path)
    # For simplicity, let's assume a linear relationship between Installed_Capacity_MW and Actual_Jobs
    # We'll train a separate model for each sector
    models = {}
    for sector in df['Sector'].unique():
        sector_df = df[df['Sector'] == sector]
        X = sector_df[['Installed_Capacity_MW']]
        y = sector_df['Actual_Jobs']
        model = LinearRegression()
        model.fit(X, y)
        models[sector] = model
    joblib.dump(models, 'mw_job_predictors.pkl')
    print('MW job prediction models trained and saved.')

def predict_jobs_from_mw(mw_capacity, sector):
    try:
        # Use relative path from the models directory
        model_path = os.path.join(os.path.dirname(__file__), 'mw_job_predictors.pkl')
        models = joblib.load(model_path)
        model = models.get(sector)
        if model:
            prediction = model.predict([[mw_capacity]])[0]
            return max(0, int(prediction)) # Ensure non-negative job predictions
        else:
            return None # Sector not found
    except FileNotFoundError:
        print("Error: MW job prediction models not found. Please train them first.")
        return None

if __name__ == '__main__':
    # Example usage:
    # Use relative path to the data directory
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs_data.csv')
    train_mw_predictor(data_path)
    print(f"Predicted jobs for Solar with 4000 MW: {predict_jobs_from_mw(4000, 'Solar')}")
    print(f"Predicted jobs for Wind with 6000 MW: {predict_jobs_from_mw(6000, 'Wind')}")



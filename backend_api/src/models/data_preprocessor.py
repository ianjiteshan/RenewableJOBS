import os
import pandas as pd
import re

def preprocess_data(csv_path):
    """
    Preprocess the renewable jobs data CSV to handle comma-separated numbers
    """
    df = pd.read_csv(csv_path)
    
    # Clean the Actual_Jobs column - remove quotes and commas
    df['Actual_Jobs'] = df['Actual_Jobs'].astype(str).str.replace('"', '').str.replace(',', '')
    df['Actual_Jobs'] = pd.to_numeric(df['Actual_Jobs'], errors='coerce')
    
    # Clean the Estimated_Jobs column if needed
    df['Estimated_Jobs'] = df['Estimated_Jobs'].astype(str).str.replace('"', '').str.replace(',', '')
    df['Estimated_Jobs'] = pd.to_numeric(df['Estimated_Jobs'], errors='coerce')
    
    # Clean the Installed_Capacity_MW column if needed
    df['Installed_Capacity_MW'] = pd.to_numeric(df['Installed_Capacity_MW'], errors='coerce')
    
    # Remove any rows with NaN values
    df = df.dropna()
    
    return df

if __name__ == '__main__':
    # Test the preprocessing
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'jobs_data.csv')
    df = preprocess_data(data_path)
    print("Data shape:", df.shape)
    print("\nFirst few rows:")
    print(df.head())
    print("\nData types:")
    print(df.dtypes)
    print("\nSectors available:")
    print(df['Sector'].unique())


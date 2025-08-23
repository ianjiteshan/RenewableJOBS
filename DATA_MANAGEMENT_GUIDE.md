# Data Management Guide
## Renewable Energy Jobs Tracker

### Overview

This guide provides comprehensive instructions on how to manage, update, and maintain the data used in the Renewable Energy Jobs Tracker application. The application is designed to work with employment data from authoritative sources like IRENA (International Renewable Energy Agency) and CEEW (Council on Energy, Environment and Water).

### Data Structure and Format

#### Required CSV Format

The application expects data in a specific CSV format with the following columns:

```csv
Year,Sector,Estimated_Jobs,Actual_Jobs,Installed_Capacity_MW
```

#### Column Descriptions

- **Year**: Integer representing the year (e.g., 2013, 2014, 2015...)
- **Sector**: String representing the renewable energy sector
- **Estimated_Jobs**: Integer representing estimated employment numbers
- **Actual_Jobs**: Integer representing actual employment numbers (can include commas and quotes)
- **Installed_Capacity_MW**: Float representing installed capacity in megawatts

#### Supported Sectors

The application currently supports the following renewable energy sectors:

1. **Solar** - Solar photovoltaic and thermal energy
2. **Wind** - Onshore and offshore wind energy
3. **Biomass** - Biomass and bioenergy
4. **Hydroelectric** - Large-scale hydroelectric power
5. **Geothermal** - Geothermal energy systems

### Data File Location

The main data file is located at:
```
renewable-jobs-app/backend_api/src/data/india_jobs_data_v2.csv
```

### How to Update Data

#### Step 1: Prepare Your Data

1. Ensure your data follows the exact CSV format specified above
2. Verify that all sectors use the exact naming convention
3. Check that years are in ascending order
4. Ensure no missing values in critical columns

#### Step 2: Data Validation

Before updating, validate your data:

- **Year Range**: Typically 2013-2023 (can be extended)
- **Sector Names**: Must match exactly (case-sensitive)
- **Numeric Values**: Estimated_Jobs and Actual_Jobs should be positive integers
- **MW Capacity**: Should be positive float values

#### Step 3: Replace the Data File

1. Navigate to the data directory:
   ```bash
   cd renewable-jobs-app/backend_api/src/data/
   ```

2. Backup the existing file (recommended):
   ```bash
   cp india_jobs_data_v2.csv india_jobs_data_v2_backup.csv
   ```

3. Replace with your new data:
   ```bash
   cp /path/to/your/new_data.csv india_jobs_data_v2.csv
   ```

#### Step 4: Retrain ML Models

After updating the data, retrain the MW prediction models:

```bash
cd renewable-jobs-app/backend_api/src/models/
python3 mw_job_predictor.py
```

#### Step 5: Restart the Application

Restart the backend application to load the new data:

```bash
cd renewable-jobs-app/backend_api/src/
python3 main.py
```

### Data Sources and Legitimacy

#### Recommended Data Sources

1. **IRENA (International Renewable Energy Agency)**
   - Website: https://www.irena.org/
   - Publications: Global Energy Transformation reports
   - Data Portal: IRENA Statistics

2. **CEEW (Council on Energy, Environment and Water)**
   - Website: https://www.ceew.in/
   - Reports: India's renewable energy employment studies
   - Research Publications: Sector-specific employment analysis

#### Data Quality Guidelines

- **Accuracy**: Use only verified data from official sources
- **Consistency**: Maintain consistent methodology across years
- **Completeness**: Ensure all required fields are populated
- **Timeliness**: Update data annually or as new reports become available

### Common Data Issues and Solutions

#### Issue 1: Comma-Separated Numbers

**Problem**: CSV contains numbers with commas (e.g., "25,000")
**Solution**: The application automatically handles this through data preprocessing

#### Issue 2: Quoted Values

**Problem**: Some values are enclosed in quotes (e.g., "38,000")
**Solution**: The preprocessing module removes quotes automatically

#### Issue 3: Missing Sectors

**Problem**: New sectors not recognized by the application
**Solution**: Update the sector icons and colors in the frontend:

```javascript
// In frontend-enhanced/src/App.jsx
const sectorIcons = {
  'Solar': Sun,
  'Wind': Wind,
  'NewSector': NewIcon, // Add new sector
  // ... existing sectors
}

const sectorColors = {
  'Solar': '#f59e0b',
  'Wind': '#06b6d4',
  'NewSector': '#color-code', // Add new color
  // ... existing sectors
}
```

#### Issue 4: Data Validation Errors

**Problem**: Application fails to load data
**Solution**: Check the console logs and verify:
- CSV format is correct
- No special characters in sector names
- All numeric fields contain valid numbers
- File encoding is UTF-8

### Advanced Data Management

#### Adding New Years

To add data for new years (e.g., 2024, 2025):

1. Follow the same CSV format
2. Ensure consistency with existing sectors
3. Update prediction year ranges in the frontend if needed

#### Adding New Sectors

To add new renewable energy sectors:

1. Add data following the CSV format
2. Update frontend sector configurations
3. Retrain ML models
4. Test all functionality

#### Data Backup Strategy

Implement a regular backup strategy:

1. **Daily Backups**: Automated backup of current data
2. **Version Control**: Use Git to track data changes
3. **Cloud Storage**: Store backups in secure cloud storage
4. **Documentation**: Maintain change logs for data updates

### API Integration

The application provides several API endpoints for data access:

- `GET /api/jobs/sectors` - Get available sectors
- `GET /api/jobs/years` - Get available years
- `GET /api/jobs/trends?sector={sector}` - Get sector trends
- `GET /api/jobs/insights?sector={sector}` - Get sector insights
- `POST /api/jobs/predict` - Predict jobs by year
- `POST /api/jobs/predict-mw` - Predict jobs by MW capacity

### Troubleshooting

#### Common Error Messages

1. **"Sector not found"**
   - Check sector name spelling and case
   - Verify sector exists in the data file

2. **"Failed to load data"**
   - Check CSV format and file permissions
   - Verify file path is correct

3. **"Prediction failed"**
   - Ensure ML models are trained
   - Check if sector has sufficient data points

#### Debug Mode

Enable debug mode for detailed error information:

```python
# In main.py
app.run(host='0.0.0.0', port=5000, debug=True)
```

### Best Practices

1. **Data Validation**: Always validate data before deployment
2. **Incremental Updates**: Add new data incrementally rather than replacing entire datasets
3. **Testing**: Test all functionality after data updates
4. **Documentation**: Document all data sources and methodologies
5. **Version Control**: Use Git to track all changes
6. **Monitoring**: Monitor application performance after data updates

### Contact and Support

For technical support or questions about data management:

- Check the application logs for error details
- Verify data format against this guide
- Test with a small dataset first
- Document any issues encountered

---

*This guide is part of the Renewable Energy Jobs Tracker project. Keep this documentation updated as the application evolves.*


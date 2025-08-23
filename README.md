


# Renewable Energy Jobs Tracker - India 🇮🇳

A visually stunning, full-stack web application for tracking, visualizing, and predicting employment trends in India's renewable energy sector. This interactive dashboard features a modern glassmorphism design, is powered by machine learning, and offers deep insights into industry data.



## 🚀 Live Demo

Experience the live application and interact with the backend API:

-   **[Frontend URL](https://renewable-jobs.vercel.app/)**


***

## ✨ Key Features

-   **Professional Data Visualizations**: Interactive and animated charts powered by **Chart.js**, including line, bar, and doughnut charts to explore trends and comparisons.
-   **Advanced MW-Based Job Prediction**: A new machine learning feature to instantly predict the number of jobs created based on a given installed capacity (MW) for any sector.
-   **Comprehensive Sector Data**: Tracks and analyzes **8 key renewable energy sectors** in India: Solar, Wind, Biomass, Hydroelectric, Geothermal, Small Hydro, Waste-to-Energy, and Bagasse Cogeneration.
-   **Modern & Responsive UI/UX**:
    -   **Glassmorphism Design**: A beautiful interface with translucent cards and gradient backgrounds.
    -   **Dark/Light Mode**: Seamless theme switching with persistent user preference.
    -   **Smooth Animations**: Fluid transitions and interactions powered by Framer Motion.
    -   **Fully Responsive**: Flawless experience on desktop, tablet, and mobile devices.
-   **Interactive Analytics Dashboard**: View real-time statistics, growth rates, capacity data, and model accuracy metrics.
-   **Data Export**: Download the underlying dataset in CSV format with a single click.

***

## 🏗️ Technical Architecture

This project is a full-stack application composed of a React frontend and a Flask backend.

| Component      | Technology                                                                                                    |
| :------------- | :------------------------------------------------------------------------------------------------------------ |
| **Frontend** | **React 18** (with Vite), **Tailwind CSS**, **shadcn/ui**, **Chart.js**, **Framer Motion**, **Lucide React** |
| **Backend** | **Flask** (Python 3.11+), **Pandas**, **CORS Enabled**, **RESTful API** |
| **ML Models** | **Scikit-learn** (Linear Regression), **Prophet** (Time-series Forecasting)                                     |
| **Deployment** | Frontend hosted on a static service (like Vercel), Backend on a VM/PaaS (like Railway, Render)                |

***

## 🛠️ Local Installation & Setup

To run this project on your local machine, follow these steps.

### Prerequisites

-   **Node.js** (v20+) with **pnpm**
-   **Python** (v3.11+) with `pip` and `venv`

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend_api

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask server (will start on [http://127.0.0.1:5001](http://127.0.0.1:5001))
python src/main.py
````

### 2\. Frontend Setup

```bash
# Navigate to the frontend directory in a new terminal
cd frontend-enhanced

# Install dependencies
pnpm install

# Run the development server (will start on http://localhost:5173)
pnpm run dev
```

Your application should now be running locally, with the frontend communicating with the local backend API.

-----

## 📁 Project Structure

```
renewable-jobs-app/
├── backend_api/                 # Main Flask backend application
│   ├── src/
│   │   ├── data/                # Datasets (CSV files)
│   │   ├── models/              # Trained ML models (.pkl)
│   │   ├── routes/              # API endpoint logic
│   │   └── main.py              # Flask app entry point
│   └── requirements.txt         # Python dependencies
├── frontend-enhanced/           # Main React frontend application
│   ├── src/
│   │   ├── components/          # Reusable React components
│   │   ├── services/            # API communication layer
│   │   └── App.jsx              # Main application component
│   └── package.json             # Node.js dependencies
├── DATA_MANAGEMENT_GUIDE.md    # Instructions for managing data
└── README.md                    # This file
```

-----

## 🤖 Machine Learning Models

The application leverages multiple models for robust predictions:

1.  **Linear Regression (`simple_linear_mw`)**:

      - **Use Case**: Powers the "MW Predict" feature.
      - **Features**: `Installed_Capacity_MW`.
      - **Target**: `Actual_Jobs`.
      - **Description**: A simple, fast model that predicts job numbers directly from megawatt capacity input.

2.  **Time-Series Forecasting (Prophet)**:

      - **Use Case**: Predicts future job trends based on historical year-over-year data.
      - **Features**: Time series (`ds`) with installed capacity as an additional regressor.
      - **Target**: `Actual_Jobs`.
      - **Description**: Ideal for forecasting with seasonality and trend analysis.

-----

## 🔌 API Endpoints

The backend exposes several RESTful endpoints. **Base URL**: `/api`

| Method | Endpoint                    | Description                                                               |
| :----- | :-------------------------- | :------------------------------------------------------------------------ |
| `GET`  | `/jobs/sectors`             | Retrieves a list of all available renewable energy sectors.               |
| `GET`  | `/jobs/years`               | Retrieves a list of all available years in the dataset.                   |
| `GET`  | `/jobs/data`                | Fetches filtered data by `sector` and/or `year`.                          |
| `GET`  | `/jobs/trends`              | Gets historical trend data for a specified `sector`.                      |
| `GET`  | `/jobs/insights`            | Provides key statistical insights for a specified `sector`.               |
| `POST` | `/jobs/predict`             | Predicts future jobs based on a `sector`, `year`, and `model_type`.       |
| `POST` | `/jobs/predict-mw`          | **(New)** Predicts jobs based on a `sector` and `installed_capacity_mw`.  |

-----

## 🚀 Deployment

The application is designed for a decoupled frontend/backend deployment.

  - **Frontend**: The React application (`frontend-enhanced` or `frontend-vercel`) is a static site built using Vite. It can be deployed to services like **Vercel**, Netlify, or GitHub Pages.
  - **Backend**: The Flask application (`backend_api`) is a long-running server process. It should be deployed to a platform that supports Python web services, such as **Railway**, **Render**, or a traditional VM.

For detailed instructions, please refer to the `VERCEL_DEPLOYMENT_GUIDE.md` and `DATA_MANAGEMENT_GUIDE.md` files.

-----

## 🤝 Contributing

Contributions are welcome\! Please follow these steps to contribute:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes and commit them (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/your-feature-name`).
5.  Open a Pull Request.

-----

## 📄 License

This project is open source and available under the **MIT License**.

-----

**Built with ❤️ for a sustainable future.**

```
```

# Render Deployment Guide for Flask Backend

This guide provides step-by-step instructions for deploying the Flask backend of the Renewable Energy Jobs Tracker application to Render.

## Why Render?

Render is a modern cloud platform that offers a simple and scalable way to deploy web applications, including Flask APIs. It supports continuous deployment from Git, custom domains, and automatic SSL.

## 🚀 Deployment Steps

### Prerequisites

1.  **Render Account**: Sign up for a free Render account at [render.com](https://render.com/).
2.  **Git Repository**: Your backend code (`backend_final` directory) should be in a Git repository (GitHub, GitLab, Bitbucket) as Render integrates directly with them.

### Step-by-Step Deployment

1.  **Prepare Your Backend Code**:
    Ensure your `backend_final` directory is structured correctly for deployment. The main application file should be `src/main.py`.

    Your `backend_final/requirements.txt` should contain:
    ```
    Flask==3.1.1
    flask-cors==6.0.0
    ```

2.  **Create a New Web Service on Render**:
    -   Log in to your Render dashboard.
    -   Click on **New** -> **Web Service**.
    -   Connect your Git repository where your `renewable-jobs-app` project is located.
    -   Select the branch you want to deploy (e.g., `main` or `master`).

3.  **Configure Your Web Service**:
    Fill in the following details:
    -   **Name**: `renewable-jobs-backend` (or your preferred name)
    -   **Region**: Choose a region close to your users.
    -   **Branch**: Select the branch you want to deploy.
    -   **Root Directory**: Set this to `backend_final` (this tells Render where your backend code is located within your repository).
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt`
    -   **Start Command**: `gunicorn --bind 0.0.0.0:$PORT src.main:app`
        *   **Note**: We use `gunicorn` as a production-ready WSGI server. Render automatically injects the `$PORT` environment variable.

4.  **Add Environment Variables (Optional but Recommended)**:
    -   Go to the **Environment** section in your service settings.
    -   You might want to add variables like `FLASK_ENV=production`.

5.  **Scaling (Optional)**:
    -   In the **Scaling** section, choose an instance type that suits your needs. For a small application, the free tier or a small paid instance will suffice.

6.  **Deploy**:
    -   Click **Create Web Service**.
    -   Render will automatically build and deploy your application. You can monitor the deployment logs in the dashboard.

## ✅ Verification

Once the deployment is successful, Render will provide you with a public URL for your backend service. You can test it by:

1.  **Visiting the URL**: Open the provided URL in your browser. You should see `{"data_loaded":true,"message":"Renewable Energy Jobs API","status":"healthy"}`.
2.  **Testing Endpoints**: Use `curl` or Postman to test specific API endpoints (e.g., `YOUR_RENDER_URL/api/jobs/sectors`).

## 🔄 Updating the Backend URL in Frontend

After deploying your backend to Render, you will get a new public URL. You **must update** the `API_BASE` variable in your frontend code (`frontend-vercel/src/services/api.js`) to point to this new Render URL.

```javascript
// frontend-vercel/src/services/api.js
const API_BASE = 'YOUR_RENDER_BACKEND_URL/api/jobs'; // Replace with your actual Render URL
```

After updating the frontend code, you will need to rebuild and redeploy your frontend application (e.g., on Vercel) for the changes to take effect.

---

**Note**: If you encounter any issues during deployment, check the Render deployment logs for detailed error messages. Ensure your `requirements.txt` is correct and all necessary dependencies are listed.


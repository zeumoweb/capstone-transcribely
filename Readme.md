# Transcribely

## Overview

[GITHUB LINK](https://github.com/zeumoweb/transcribely)

Transcribely is a web application designed to make video accessible to all audiences through subtitling, translation, and dubbing. The application features a Flask-based backend with MongoDB for data storage and a React.js frontend for the user interface.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [Running the Application](#running-the-application)
  - [Running Backend](#running-backend)
  - [Running Frontend](#running-frontend)
- [Environment Variables](#environment-variables)
- [Troubleshooting](#troubleshooting)

## Project Structure

```
transcribely/
│
├── backend/
│   ├── myapp.py
│   ├── requirements.txt
│   ├── config.py
│   ├── routes/
│   ├── models/
│   ├── utils/
|   ├── .env
│   └── ...
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── taildwind.config.js
│   └── ...
│
├── README.md
└── ...
```

- **`backend/`**: Contains all the Flask-related code, including routes, models, and utility functions.
- **`frontend/`**: Contains the React.js code for the user interface.
- **`README.md`**: This file.

## Prerequisites

Before setting up Transcribely, ensure that the following software is installed on your system:

1. **Python 3.8+**: For running the Flask backend.
2. **Node.js 14+ and npm**: For managing and running the React frontend.
3. **MongoDB**: As the database for storing user data, transcriptions, and translations.
4. **Git**: For version control.

Additionally, you will need to create API keys for the following services:

1. **Google Cloud Text-to-Speech API**
2. **Google Cloud Translate API**
2. **Assemby AI**

## Setup Instructions

### Backend Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/zeumoweb/transcribely.git
   cd transcribely/backend
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB:**

   - Ensure MongoDB is running on your local machine or a server.
   - Update the MongoDB connection string in `config.py` or through environment variables.

5. **Set up environment variables:**

   Create a `.env` file in the `backend` directory and add the following:

   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   MONGO_URI=mongodb://localhost:27017/transcribely
   GOOGLE_API_KEY=<your-google-api-key>
   SECRET_KEY=<your-secret-key>
   ```

6. **Initialize the database:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
7. **Alternatively, use Mongodb cloud**


### Frontend Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Set up environment variables:**

   Create a `.env` file in the `frontend` directory and add the following:

   ```bash
   REACT_APP_BACKEND_URL=http://localhost:5000/api
   REACT_APP_GOOGLE_API_KEY=<your-google-api-key>
   ```

## Running the Application

### Running Backend

1. **Activate the virtual environment:**

   ```bash
   cd backend
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. **Run the Flask server:**

   ```bash
   flask run
   ```

   The backend should now be running on `http://localhost:5000`.

### Running Frontend

1. **Navigate to the frontend directory:**

   ```bash
   cd ../frontend
   ```

2. **Start the React development server:**

   ```bash
   npm start
   ```

   The frontend should now be accessible at `http://localhost:3000`.

## Environment Variables

The following environment variables are used in the project:

- **Backend:**
  - `FLASK_APP`: The entry point for the Flask application.
  - `FLASK_ENV`: The environment mode (development/production).
  - `MONGO_URI`: The MongoDB connection string.
  - `GOOGLE_API_KEY`: The API key for Google services.
  - `SECRET_KEY`: A secret key for session management and other purposes.

- **Frontend:**
  - `REACT_APP_BACKEND_URL`: The URL of the backend API.
  - `REACT_APP_GOOGLE_API_KEY`: The API key for Google services.



## Troubleshooting
- **MongoDB Connection Issues**: Ensure MongoDB is running and accessible at the URI specified.
- **Google API Errors**: Check your API keys and quotas on the Google Cloud Console.
- **CORS Issues**: Ensure that CORS is properly configured in the Flask backend for cross-origin requests from the React frontend.

For any issues or bugs, please open an issue on the GitHub repository.

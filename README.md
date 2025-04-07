# SHL Assessment Recommender

## Project Description
This web application recommends SHL individual test solutions based on job descriptions or natural language queries.

## Prerequisites
- Python 3.8+
- pip (Python package manager)

## Setup Instructions

### Backend Setup
1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the backend server
```bash
python app.py
```

### Frontend
- Simply open the `index.html` file in a web browser
- Ensure backend is running on `http://localhost:5000`

## How to Use
1. Enter a job description or keywords in the input field
2. Click "Recommend Assessments"
3. View the top recommended SHL assessments

## Features
- Natural language query input
- Intelligent assessment recommendation
- Tabular display of top 10 relevant assessments
- Links to SHL assessment catalog
- Remote testing and adaptive test support indicators

## Technology Stack
- Backend: Python, Flask
- Frontend: HTML, JavaScript
- NLP: scikit-learn (TF-IDF)

## Troubleshooting
- Ensure all dependencies are installed
- Check that the backend server is running
- Verify CORS settings if encountering cross-origin issues
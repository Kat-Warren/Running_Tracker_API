# Running_Tracker_API

# Overview 
This API using Python, FastAPI, SQLite and SQLAlchemy to create a RESTful web service application
It enables users to log and analyse their running performance. 
Additionly to the CRUD functionality, my system integrates a real-world dataset to show how the individual performance compares to professionaly benchmarking. This enables the users to compare their runs to elite levels based on event, age and gender. It also has the functionality to compare your performance to historical self performances. 

# System Architecture
Backend: Fast API (Python)
Database: SQLite
Froundend: HTML, CSS, JavaScprit
Chars: Chart.js
Tests: Pytest

# Installation & Setup
Dependencies: pip install -r requirements.txt
Running App: py -m uvicorn app.main:app --reload
Browser: http://127.0.0.1:8000
Documentation: http://127.0.0.1:8000/docs

# Testing
py -m pytest tests
Tests include:
- CRUD operation
- Validation errors
- Missing resources
- Comparison endpoint behaviours

# API Endpoints
POST /runs → Create a run
GET /runs → Get all runs
GET /runs/{id} → Get a single run
PUT /runs/{id} → Update a run
DELETE /runs/{id} → Delete a run
GET /compare/{id} → Compare run to elite and personal data

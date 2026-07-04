# 2. Requirement Analysis

## Functional Requirements
- Accept 7 numeric inputs: Nitrogen (N), Phosphorous (P), Potassium (K), temperature, humidity, pH, rainfall
- Validate inputs (realistic ranges, no missing/non-numeric values)
- Predict the most suitable crop using a trained ML model
- Display top-5 crop confidence scores
- Provide fertilizer adjustment advice based on the recommended crop
- Provide a soil health score (0–100)
- Allow comparison between two crops for the same conditions
- Provide dataset visualizations (dashboard)
- Provide K-Means clustering insights for research use cases
- Allow downloading the recommendation as a PDF report
- Support live weather autofill via geolocation

## Non-Functional Requirements
- Response time: prediction should return in under 1 second
- Usability: simple web form, no technical knowledge required
- Portability: runs locally (Windows/Linux/macOS) and is deployable to the cloud
- Maintainability: modular code (separate model training, analysis, and web app)

## Hardware Requirements
- Processor: Intel Core i3 or above
- RAM: Minimum 4 GB
- Storage: Minimum 10 GB free space
- Internet connection (for downloading datasets/packages and live weather autofill)

## Software Requirements
- OS: Windows / Linux / macOS
- Python 3.10+
- VS Code (or any code editor)
- Git & GitHub account
- Browser (Chrome/Edge/Firefox)

## Required Libraries
See `requirements.txt` in the **5. Project Development** folder:
- Flask, Gunicorn (backend & deployment)
- scikit-learn, pandas, NumPy (machine learning & data processing)
- Matplotlib, Seaborn (visualization)
- ReportLab (PDF generation)

## Dataset Requirement
A labeled dataset containing soil/environmental readings and the correct crop label — sourced as the "Crop Recommendation Dataset" (2,200 rows, 22 crop classes, no missing values).

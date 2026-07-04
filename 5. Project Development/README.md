# 5. Project Development — Source Code

This folder contains the full working Flask application.

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
python model/analysis.py     # generates dashboard/research charts
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Structure
```
app.py               Flask application (all routes)
requirements.txt     Python dependencies
Procfile             Deployment start command (gunicorn)
dataset/             Crop_recommendation.csv (2200 rows, 22 crops)
model/
  train_model.py     Trains & compares KNN, Logistic Regression, Decision Tree, Random Forest
  analysis.py        Generates dashboard charts + K-Means clustering insights
  *.pkl              Trained model, scaler, encoder, and precomputed stats
templates/           Jinja2 HTML templates (Bootstrap + Chart.js)
static/              CSS and generated chart images
```

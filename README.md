# 🌱 OptiCrop — Smart Agricultural Production Optimization Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Model-orange?logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

**Live Demo:** [opticrop-utog.onrender.com](https://opticrop-utog.onrender.com)
**GitHub:** [github.com/bhargavi-jpg/opticrop](https://github.com/bhargavi-jpg/opticrop)

> A machine learning-based web application that recommends the most suitable crop to grow based on soil nutrients (N, P, K) and environmental conditions (temperature, humidity, pH, rainfall) — helping farmers make data-driven decisions instead of relying on guesswork.

---

## 📌 Problem Statement

Farmers often choose crops based on tradition or intuition rather than actual soil and climate data, which can lead to poor yields and inefficient use of fertilizer, water, and land. OptiCrop solves this by using a trained machine learning model to recommend the best-suited crop for a given set of soil and weather conditions — instantly, through a simple web interface.

## ✨ Features

- 🌾 **Crop Recommendation** — enter 7 soil/environmental readings, get an instant ML-powered crop suggestion
- 📊 **Confidence Chart** — see the top 5 most likely crops with confidence percentages
- 🧪 **Fertilizer Advice** — compares your N/P/K to the ideal average for the recommended crop and tells you what to adjust
- 💯 **Soil Health Score** — a 0–100 score showing how close your soil is to the recommended crop's ideal profile
- ⚖️ **Compare Crops** — compare two crops side-by-side against one set of conditions, with a radar chart
- 📈 **Dashboard** — exploratory data visualizations (NPK-by-crop, correlation heatmap, rainfall vs temperature)
- 🔬 **Research Insights** — K-Means clustering of crops by environmental similarity, for research/policy use cases
- 📍 **Live Weather Autofill** — auto-fills temperature, humidity, and rainfall using your device's location (Open-Meteo API)
- 📄 **PDF Report Download** — download your recommendation, score, and fertilizer advice as a clean PDF
- ✅ **Input Validation** — rejects unrealistic values (e.g. pH > 14) with clear error messages

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Gunicorn |
| Machine Learning | scikit-learn (KNN, Logistic Regression, Decision Tree, Random Forest, K-Means, PCA) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Chart.js |
| Frontend | HTML5, CSS3, Bootstrap 5, Jinja2 |
| PDF Generation | ReportLab |
| Weather Data | Open-Meteo API (free, no key required) |
| Deployment | Render (Gunicorn WSGI server) |
| Version Control | Git & GitHub |

## 🧠 Machine Learning Approach

Four classification algorithms were trained and compared on an 80/20 train-test split using a dataset of 2,200 samples across 22 crop types:

| Model | Accuracy |
|---|---|
| **Random Forest** ✅ | **99.55%** |
| KNN (k=5) | 97.95% |
| Decision Tree | 97.95% |
| Logistic Regression | 97.27% |

Random Forest was selected for deployment. K-Means clustering (unsupervised) is used separately in the **Research Insights** page to group crops by environmental similarity — supporting exploratory research rather than direct prediction.

## 📂 Project Structure

```
OptiCrop/
├── app.py                  # Flask application (routes, prediction logic)
├── requirements.txt        # Python dependencies
├── Procfile                 # Deployment start command (gunicorn)
├── README.md
├── dataset/
│   └── Crop_recommendation.csv
├── model/
│   ├── train_model.py      # Trains & compares ML models
│   ├── analysis.py         # Generates dashboard charts + K-Means insights
│   ├── crop_model.pkl      # Trained Random Forest model
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   ├── crop_stats.pkl
│   ├── cluster_summary.pkl
│   └── feature_ranges.pkl
├── templates/
│   ├── index.html
│   ├── result.html
│   ├── compare.html
│   ├── dashboard.html
│   └── research.html
└── static/
    ├── style.css
    └── charts/              # Generated visualization images
```

## 🚀 Getting Started (Local Setup)

```bash
# Clone the repo
git clone https://github.com/bhargavi-jpg/opticrop.git
cd opticrop

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Generate charts & analysis data
python model/analysis.py

# Run the app
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## 🌐 Deployment

Deployed on [Render](https://render.com) using Gunicorn as the production WSGI server.

- **Build Command:** `pip install -r requirements.txt && python model/analysis.py`
- **Start Command:** `gunicorn app:app`

## 📸 Screenshots

_Add screenshots of the Recommend, Compare, Dashboard, and Research Insights pages here._

## 🔮 Future Scope

- Deploy on a paid tier to remove free-tier cold-start delays
- Add yield estimation (regression model)
- Multi-language support for wider farmer accessibility
- User accounts with prediction history

## 👥 Team

| Name | Role |
|---|---|
| Faseeha Iffat Shaik | Team Lead |
| Jahnavi Jampani | Member |
| Manoj Praveen Bejawada | Member |
| Evuri Bhargavi | Member |
| Sai Harshith Myla | Member |

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

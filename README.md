# 🌱 OptiCrop — Smart Agricultural Production Optimization Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Model-orange?logo=scikitlearn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

**Live Demo:** [opticrop-utog.onrender.com](https://opticrop-utog.onrender.com)

> A machine learning-based web application that recommends the most suitable crop to grow based on soil nutrients (N, P, K) and environmental conditions (temperature, humidity, pH, rainfall) — helping farmers make data-driven decisions instead of relying on guesswork.

This repository is organized by project phase, following the standard project lifecycle:

| Folder | Contents |
|---|---|
| [1. Brainstorming & Ideation](<1. Brainstorming & Ideation>) | Problem statement, idea, use-case scenarios |
| [2. Requirement Analysis](<2. Requirement Analysis>) | Functional/non-functional requirements, hardware & software needs |
| [3. Project Design](<3. Project Design>) | System architecture, data flow, module & UI design |
| [4. Project Planning](<4. Project Planning>) | Module breakdown, tools used, team roles |
| [5. Project Development](<5. Project Development>) | **Full working source code** (Flask app, ML model, frontend) |
| [6. Project Testing](<6. Project Testing>) | Model evaluation results & functional test cases |
| [7. Project Documentation](<7. Project Documentation>) | Detailed project overview & Word report |
| [8. Project Demonstration](<8. Project Demonstration>) | Live demo link, walkthrough guide, screenshots |

## Quick Start

The runnable application lives in **`5. Project Development/`**:

```bash
cd "5. Project Development"
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
python model/analysis.py
python app.py
```

Then open `http://127.0.0.1:5000`.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Gunicorn |
| Machine Learning | scikit-learn (KNN, Logistic Regression, Decision Tree, Random Forest, K-Means, PCA) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Chart.js |
| Frontend | HTML5, CSS3, Bootstrap 5, Jinja2 |
| PDF Generation | ReportLab |
| Weather Data | Open-Meteo API |
| Deployment | Render |

## Team

| Name | Role |
|---|---|
| Bhargavi | Team Member |
| Manoj Praveen Bejawada | Team Member |

## License

MIT License — see [LICENSE](LICENSE).

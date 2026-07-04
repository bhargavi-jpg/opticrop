# OptiCrop — Full VS Code Setup & Run Guide

This project is 100% ready to run. Everything described in your Technical
Architecture doc has already been built for you:

- `dataset/Crop_recommendation.csv` — 2200 rows, 22 crops, N/P/K/temperature/humidity/ph/rainfall
- `model/train_model.py` — trains & compares KNN, Logistic Regression, Decision Tree, Random Forest
- `model/crop_model.pkl`, `scaler.pkl`, `label_encoder.pkl` — already trained (Random Forest, 99.55% accuracy)
- `app.py` — Flask backend
- `templates/index.html`, `templates/result.html` — Bootstrap frontend
- `static/style.css` — styling

You only need Python + VS Code. No Jupyter/Anaconda required.

---

## 1. What to install (one-time)

| Tool | Where to get it |
|---|---|
| Python 3.10+ | https://www.python.org/downloads/ (check "Add to PATH" during install) |
| VS Code | https://code.visualstudio.com/ |
| VS Code Python extension | Open VS Code → Extensions icon (left sidebar) → search "Python" → Install (by Microsoft) |

Verify Python is installed — open a terminal (Windows: `cmd`/PowerShell, Mac/Linux: Terminal) and run:
```bash
python --version
```
(On Mac/Linux it may be `python3 --version`.)

---

## 2. Open the project in VS Code

1. Unzip the `OptiCrop` folder you downloaded anywhere on your computer (e.g. Desktop).
2. Open VS Code → **File → Open Folder** → select the `OptiCrop` folder.
3. Open a terminal **inside VS Code**: menu **Terminal → New Terminal** (or `` Ctrl+` ``).
   All commands below are typed into this terminal, with the folder open as your working directory.

Your folder structure looks like this:
```
OptiCrop/
├── app.py                     ← Flask entry point, run this to start the site
├── requirements.txt           ← list of Python packages needed
├── dataset/
│   └── Crop_recommendation.csv
├── model/
│   ├── train_model.py         ← run this to retrain the model
│   ├── crop_model.pkl         ← trained model (already generated)
│   ├── scaler.pkl
│   └── label_encoder.pkl
├── templates/
│   ├── index.html             ← input form page
│   └── result.html            ← prediction result page
└── static/
    └── style.css
```

---

## 3. Create a virtual environment (keeps packages isolated)

In the VS Code terminal:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You'll know it worked because your terminal prompt now starts with `(venv)`.

> If VS Code pops up "Select Interpreter", choose the one inside `venv` (e.g. `./venv/bin/python`).

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, pandas, numpy, scikit-learn, matplotlib, seaborn.

---

## 5. (Optional) Retrain the model yourself

The trained `.pkl` files are already included, so you can skip this step.
But if you want to see the training process, compare model accuracies, or
retrain after changing the dataset:

```bash
python model/train_model.py
```

This will:
1. Load `dataset/Crop_recommendation.csv`
2. Split into train/test (80/20)
3. Scale features with `StandardScaler`
4. Train KNN, Logistic Regression, Decision Tree, Random Forest
5. Print an accuracy comparison table
6. Save the best model as `model/crop_model.pkl` (overwrites the existing one)

---

## 6. Run the Flask web app

```bash
python app.py
```

You'll see terminal output like:
```
 * Running on http://127.0.0.1:5000
```

Open that URL (`http://127.0.0.1:5000`) in your browser (Ctrl+click the link
in the VS Code terminal, or copy-paste it into Chrome/Edge/Firefox).

The app now has 5 pages, linked in the navbar:

- **Recommend** (`/`) — enter N, P, K, Temperature, Humidity, pH, Rainfall and
  get a recommended crop, a top-5 confidence bar chart, a soil health score
  (0-100, how close your soil is to that crop's ideal profile), and
  fertilizer advice. A **"Use My Location's Weather"** button auto-fills
  temperature, humidity, and a 7-day rainfall total using your device's GPS
  and the free Open-Meteo weather API (no API key needed; requires you to
  allow location access in the browser).
- **Compare Crops** (`/compare`) — pick two crops and one set of conditions;
  see a suitability score for each and a radar chart comparing your
  conditions against both crops' ideal profiles.
- **Dashboard** (`/dashboard`) — exploratory charts: average NPK needs per
  crop, a feature correlation heatmap, and a rainfall-vs-temperature scatter
  plot for a few crops.
- **Research Insights** (`/research`) — K-Means clustering (k=6) of all crops
  by environmental similarity, visualized with PCA, plus a table showing
  which crops dominate each cluster. This covers Scenario 3 (research &
  policy planning) and the K-Means item from the original spec.
- **Download PDF Report** — on the result page, click "Download PDF Report"
  to get a clean PDF with the recommended crop, soil health score, your
  inputs, the top-5 confidence table, and fertilizer advice — useful to
  save or hand to a farmer.

Input validation checks realistic ranges (e.g. pH between 0-14, humidity
between 0-100) and shows a clear error message without losing what you
already typed.

To regenerate the dashboard/research charts and fertilizer stats after
changing the dataset:
```bash
python model/analysis.py
```

To stop the server: click in the terminal and press `Ctrl+C`.

---

## 7. Sample values to test with

| Crop | N | P | K | Temp | Humidity | pH | Rainfall |
|---|---|---|---|---|---|---|---|
| Rice | 90 | 42 | 43 | 20.9 | 82.0 | 6.5 | 202.9 |
| Coffee | 101 | 30 | 30 | 25.5 | 58.9 | 6.8 | 158.1 |
| Watermelon | 99 | 17 | 50 | 25.6 | 85.2 | 6.5 | 50.7 |

---

## 8. Common issues

- **`python : command not found`** → reinstall Python and check "Add to PATH".
- **`pip install` fails / permission error** → make sure your `venv` is activated (prompt shows `(venv)`); if not, re-run the activate command from step 3.
- **Port 5000 already in use** → edit the last line of `app.py` to `app.run(debug=True, port=5001)`, then visit `http://127.0.0.1:5001`.
- **Templates not found error** → make sure you run `python app.py` from inside the `OptiCrop` root folder, not from inside `templates/` or `model/`.
- **Module not found (flask/pandas/sklearn)** → your venv isn't activated, or `pip install -r requirements.txt` didn't finish — re-run step 3 then step 4.

---

## 9. Where each requirement from your spec is implemented

| Spec item | File |
|---|---|
| Environment setup | `requirements.txt`, this README |
| ML model selection/training (KNN, Logistic Regression, Decision Tree, Random Forest) | `model/train_model.py` |
| Model persistence (.pkl) | `model/crop_model.pkl`, `scaler.pkl`, `label_encoder.pkl` |
| Backend (Flask, prediction logic, input validation) | `app.py` |
| Frontend (HTML/CSS/Bootstrap form + results) | `templates/index.html`, `templates/result.html`, `static/style.css` |
| Testing | Section 7 sample values above; Flask dev server (`debug=True`) shown live in browser |

*(Note: K-Means Clustering from the spec is an unsupervised method — useful for exploring crop groupings but not for label prediction, so it wasn't used for the final deployed classifier. It could be added as a separate exploratory notebook cell in `model/train_model.py` if your mentor wants it for the research/EDA angle in Scenario 3.)*

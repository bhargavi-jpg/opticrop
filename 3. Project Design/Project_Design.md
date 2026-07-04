# 3. Project Design

## System Architecture

```
                ┌───────────────────────┐
                │   User's Browser       │
                │ (HTML/CSS/Bootstrap,   │
                │  Chart.js, JS geoloc.) │
                └───────────┬───────────┘
                            │ HTTP request (form submit)
                            ▼
                ┌───────────────────────┐
                │   Flask Backend        │
                │  (app.py)              │
                │  - Input validation    │
                │  - Feature scaling     │
                │  - Model inference     │
                │  - Fertilizer logic    │
                │  - PDF generation      │
                └───────────┬───────────┘
                            │ loads at startup
                            ▼
        ┌────────────────────────────────────┐
        │        model/ (trained artifacts)   │
        │  crop_model.pkl   (Random Forest)   │
        │  scaler.pkl       (StandardScaler)  │
        │  label_encoder.pkl                  │
        │  crop_stats.pkl, cluster_summary.pkl│
        │  feature_ranges.pkl                 │
        └────────────────────────────────────┘
```

## Data Flow
1. User submits soil & environmental readings via the web form
2. Flask validates the input ranges
3. Input is scaled using the same `StandardScaler` fitted during training
4. The trained Random Forest model predicts the crop label
5. The label is decoded back to a crop name via `LabelEncoder`
6. Fertilizer advice and soil health score are computed by comparing user input to the crop's historical average
7. Results (crop, confidence chart, advice, score) are rendered back to the user

## Module Design
| Module | Responsibility |
|---|---|
| `model/train_model.py` | Preprocessing, model training & comparison, persistence |
| `model/analysis.py` | EDA charts, K-Means clustering, feature ranges |
| `app.py` | Routing, validation, prediction, PDF generation |
| `templates/*.html` | Presentation layer (Jinja2 + Bootstrap + Chart.js) |
| `static/` | CSS and generated chart images |

## Database Design
No database is used — the system is stateless per request, with the trained model and precomputed statistics loaded from `.pkl` files at startup. Session storage (Flask session) is used only to temporarily hold the last prediction for PDF export.

## UI Design
- **Recommend page** — input form + live weather autofill button
- **Result page** — recommended crop, soil health bar, confidence chart, fertilizer advice, PDF download
- **Compare page** — two-crop dropdown + radar chart
- **Dashboard page** — static EDA charts
- **Research Insights page** — K-Means cluster visualization + table

# 6. Project Testing

## Testing Approach
The application was tested using Flask's built-in test client (automated) and manually through the browser, covering functional correctness, input validation, and each feature end-to-end.

## Model Evaluation (Test Set — 20% holdout)
| Model | Test Accuracy |
|---|---|
| **Random Forest** (deployed) | **99.55%** |
| KNN (k=5) | 97.95% |
| Decision Tree | 97.95% |
| Logistic Regression | 97.27% |

## Functional Test Cases

| # | Test Case | Input | Expected Result | Actual Result |
|---|---|---|---|---|
| 1 | Valid prediction (Rice profile) | N=90, P=42, K=43, Temp=20.9, Humidity=82, pH=6.5, Rainfall=202.9 | Recommends Rice | ✅ Pass — Rice |
| 2 | Valid prediction (Coffee profile) | N=101, P=30, K=30, Temp=25.5, Humidity=58.9, pH=6.8, Rainfall=158.1 | Recommends Coffee | ✅ Pass — Coffee |
| 3 | Valid prediction (Watermelon profile) | N=99, P=17, K=50, Temp=25.6, Humidity=85.2, pH=6.5, Rainfall=50.7 | Recommends Watermelon | ✅ Pass — Watermelon |
| 4 | Invalid pH (out of range) | pH=25 | Rejected with clear error message | ✅ Pass |
| 5 | Negative Nitrogen | N=-5 | Rejected with clear error message | ✅ Pass |
| 6 | Non-numeric input | N="abc" | Rejected with "must be a number" error | ✅ Pass |
| 7 | Missing field | temperature left blank | Rejected with "please enter a value" error | ✅ Pass |
| 8 | PDF report download | After valid prediction | Downloads a correctly formatted PDF | ✅ Pass |
| 9 | Crop comparison (different crops) | Rice vs Maize | Returns suitability scores + radar chart | ✅ Pass |
| 10 | Crop comparison (same crop selected twice) | Rice vs Rice | Rejected with "choose two different crops" error | ✅ Pass |
| 11 | Dashboard page loads | GET `/dashboard` | Returns 200, displays 3 charts | ✅ Pass |
| 12 | Research Insights page loads | GET `/research` | Returns 200, displays cluster chart + table | ✅ Pass |

## Route-Level Automated Tests
All routes (`/`, `/predict`, `/dashboard`, `/research`, `/compare`, `/download_report`) were verified using Flask's test client to return HTTP 200 and the expected content, across valid inputs, invalid inputs, and edge cases (missing fields, out-of-range values, identical crop selection).

## Deployment Testing
- Verified the app runs correctly under **Gunicorn** (production WSGI server) locally before deployment
- Verified the live deployed app (Render) loads all pages and static chart images correctly

"""
OptiCrop - Flask Web Application
---------------------------------
Routes:
  /                 Input form (with validation + weather autofill)
  /predict          Crop prediction + fertilizer advice + confidence chart + soil health score
  /download_report  Downloads the last prediction as a PDF
  /dashboard        Dataset visualizations (EDA)
  /research         K-Means clustering insights (Scenario 3 - research/policy)
  /compare          Compare two crops against one set of soil/environmental conditions

Run with:
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import io
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, session, send_file

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

app = Flask(__name__)
app.secret_key = "opticrop-dev-secret-key"  # fine for local/dev use

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "model")

# ---------------------------------------------------------------------
# Load trained model + preprocessing objects + analysis data once at startup
# ---------------------------------------------------------------------
with open(os.path.join(MODEL_DIR, "crop_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)

with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "rb") as f:
    label_encoder = pickle.load(f)

with open(os.path.join(MODEL_DIR, "crop_stats.pkl"), "rb") as f:
    crop_stats = pickle.load(f)  # {crop_name: {N, P, K, temperature, humidity, ph, rainfall}}

with open(os.path.join(MODEL_DIR, "cluster_summary.pkl"), "rb") as f:
    cluster_summary = pickle.load(f)  # {cluster_id: [top crops]}

with open(os.path.join(MODEL_DIR, "feature_ranges.pkl"), "rb") as f:
    feature_ranges = pickle.load(f)  # {feature: (min, max)}

FEATURE_ORDER = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
ALL_CROPS = sorted(crop_stats.keys())

VALID_RANGES = {
    "N": (0, 300, "Nitrogen"),
    "P": (0, 300, "Phosphorous"),
    "K": (0, 300, "Potassium"),
    "temperature": (-10, 60, "Temperature (°C)"),
    "humidity": (0, 100, "Humidity (%)"),
    "ph": (0, 14, "Soil pH"),
    "rainfall": (0, 500, "Rainfall (mm)"),
}


def validate_inputs(form):
    values = {}
    for feature in FEATURE_ORDER:
        raw = form.get(feature, "").strip()
        low, high, label = VALID_RANGES[feature]
        if raw == "":
            return None, f"Please enter a value for {label}."
        try:
            val = float(raw)
        except ValueError:
            return None, f"{label} must be a number."
        if not (low <= val <= high):
            return None, f"{label} should be between {low} and {high}. You entered {val}."
        values[feature] = val
    return values, None


def fertilizer_advice(crop_name, user_values):
    stats = crop_stats.get(crop_name)
    if not stats:
        return []
    advice = []
    labels = {"N": "Nitrogen", "P": "Phosphorous", "K": "Potassium"}
    for nutrient in ["N", "P", "K"]:
        ideal = stats[nutrient]
        actual = user_values[nutrient]
        diff = ideal - actual
        threshold = max(5, ideal * 0.10)
        if diff > threshold:
            advice.append(f"Increase {labels[nutrient]} by ~{diff:.0f} units (ideal avg: {ideal:.0f}, yours: {actual:.0f}).")
        elif diff < -threshold:
            advice.append(f"Reduce {labels[nutrient]} by ~{abs(diff):.0f} units (ideal avg: {ideal:.0f}, yours: {actual:.0f}).")
    if not advice:
        advice.append("Your N, P, and K levels are already close to ideal for this crop. No major fertilizer adjustment needed.")
    return advice


def soil_health_score(crop_name, user_values):
    """
    Score 0-100: how close the entered N, P, K, pH values are to the
    recommended crop's ideal averages, normalized against the dataset's
    overall min-max range for each feature.
    """
    stats = crop_stats.get(crop_name)
    if not stats:
        return 100
    soil_features = ["N", "P", "K", "ph"]
    penalties = []
    for feat in soil_features:
        ideal = stats[feat]
        actual = user_values[feat]
        low, high = feature_ranges[feat]
        span = max(high - low, 1e-6)
        deviation_pct = abs(actual - ideal) / span * 100
        penalties.append(min(deviation_pct, 100))
    avg_penalty = sum(penalties) / len(penalties)
    score = max(0, round(100 - avg_penalty))
    return score


def suitability_score(crop_name, user_values):
    """0-100 suitability of a crop for the given conditions, across all 7 features."""
    stats = crop_stats.get(crop_name)
    if not stats:
        return 0
    penalties = []
    for feat in FEATURE_ORDER:
        ideal = stats[feat]
        actual = user_values[feat]
        low, high = feature_ranges[feat]
        span = max(high - low, 1e-6)
        deviation_pct = abs(actual - ideal) / span * 100
        penalties.append(min(deviation_pct, 100))
    avg_penalty = sum(penalties) / len(penalties)
    return max(0, round(100 - avg_penalty))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    values, error = validate_inputs(request.form)
    if error:
        return render_template("index.html", error=error, prev=request.form)

    try:
        input_df = pd.DataFrame([values], columns=FEATURE_ORDER)
        input_scaled = scaler.transform(input_df)

        prediction_encoded = model.predict(input_scaled)[0]
        crop_name = label_encoder.inverse_transform([prediction_encoded])[0]

        probabilities = model.predict_proba(input_scaled)[0]
        top_idx = np.argsort(probabilities)[::-1][:5]
        top_crops = [label_encoder.inverse_transform([i])[0].capitalize() for i in top_idx]
        top_confidences = [round(probabilities[i] * 100, 1) for i in top_idx]

        advice = fertilizer_advice(crop_name, values)
        health_score = soil_health_score(crop_name, values)

        # Save to session so /download_report can regenerate the same result as a PDF
        session["last_result"] = {
            "crop": crop_name.capitalize(),
            "inputs": values,
            "advice": advice,
            "health_score": health_score,
            "top_crops": top_crops,
            "top_confidences": top_confidences,
        }

        return render_template(
            "result.html",
            crop=crop_name.capitalize(),
            top_crops=top_crops,
            top_confidences=top_confidences,
            inputs=values,
            advice=advice,
            health_score=health_score,
        )

    except Exception as e:
        return render_template("index.html", error=f"Something went wrong: {e}", prev=request.form)


@app.route("/download_report")
def download_report():
    data = session.get("last_result")
    if not data:
        return render_template("index.html", error="No recent recommendation found. Please submit the form first.")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("TitleGreen", parent=styles["Title"], textColor=colors.HexColor("#2E7D32"))
    heading_style = ParagraphStyle("Heading", parent=styles["Heading2"], textColor=colors.HexColor("#1B1B1B"))

    elements = []
    elements.append(Paragraph("OptiCrop - Crop Recommendation Report", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Recommended Crop: <b>{data['crop']}</b>", styles["Heading1"]))
    elements.append(Paragraph(f"Soil Health Score: <b>{data['health_score']} / 100</b>", styles["Normal"]))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Input Conditions", heading_style))
    input_rows = [["Parameter", "Value"]] + [[k, str(v)] for k, v in data["inputs"].items()]
    t1 = Table(input_rows, colWidths=[8 * cm, 8 * cm])
    t1.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Top 5 Crop Confidence", heading_style))
    conf_rows = [["Crop", "Confidence (%)"]] + [
        [c, f"{p}%"] for c, p in zip(data["top_crops"], data["top_confidences"])
    ]
    t2 = Table(conf_rows, colWidths=[8 * cm, 8 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E7D32")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 16))

    elements.append(Paragraph("Fertilizer Advice", heading_style))
    for tip in data["advice"]:
        elements.append(Paragraph(f"&bull; {tip}", styles["Normal"]))
        elements.append(Spacer(1, 4))

    doc.build(elements)
    buffer.seek(0)
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"OptiCrop_Report_{data['crop']}.pdf",
        mimetype="application/pdf",
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/research")
def research():
    return render_template("research.html", cluster_summary=cluster_summary)


@app.route("/compare", methods=["GET", "POST"])
def compare():
    if request.method == "GET":
        return render_template("compare.html", crops=ALL_CROPS)

    crop_a = request.form.get("crop_a")
    crop_b = request.form.get("crop_b")
    values, error = validate_inputs(request.form)

    if error:
        return render_template("compare.html", crops=ALL_CROPS, error=error, prev=request.form)
    if crop_a == crop_b:
        return render_template("compare.html", crops=ALL_CROPS, error="Please choose two different crops to compare.", prev=request.form)

    score_a = suitability_score(crop_a, values)
    score_b = suitability_score(crop_b, values)
    winner = crop_a.capitalize() if score_a > score_b else (crop_b.capitalize() if score_b > score_a else "Tie")

    radar_labels = FEATURE_ORDER
    radar_a = [crop_stats[crop_a][f] for f in FEATURE_ORDER]
    radar_b = [crop_stats[crop_b][f] for f in FEATURE_ORDER]
    radar_user = [values[f] for f in FEATURE_ORDER]

    return render_template(
        "compare.html",
        crops=ALL_CROPS,
        result=True,
        crop_a=crop_a.capitalize(),
        crop_b=crop_b.capitalize(),
        score_a=score_a,
        score_b=score_b,
        winner=winner,
        radar_labels=radar_labels,
        radar_a=radar_a,
        radar_b=radar_b,
        radar_user=radar_user,
        prev=request.form,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

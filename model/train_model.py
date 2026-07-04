"""
OptiCrop - Model Training Script
---------------------------------
Trains and compares KNN, Logistic Regression, Decision Tree, and Random
Forest on the crop recommendation dataset, then saves the best model
(along with the fitted StandardScaler and LabelEncoder) as .pkl files
inside the model/ folder so the Flask app can load them at prediction time.

Run this file directly:
    python model/train_model.py
"""

import pandas as pd
import numpy as np
import pickle
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "dataset", "Crop_recommendation.csv")

# ---------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
print("Dataset shape:", df.shape)
print(df.head())

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET = "label"

X = df[FEATURES]
y = df[TARGET]

# ---------------------------------------------------------------------
# 2. Encode target labels (rice -> 0, maize -> 1, ...)
# ---------------------------------------------------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# ---------------------------------------------------------------------
# 3. Train / test split
# ---------------------------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# ---------------------------------------------------------------------
# 4. Feature scaling (helps KNN & Logistic Regression the most)
# ---------------------------------------------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ---------------------------------------------------------------------
# 5. Train & compare models
# ---------------------------------------------------------------------
models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
}

results = {}
best_model_name = None
best_model = None
best_accuracy = 0.0

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, preds)
    results[name] = acc
    print(f"\n{name} Accuracy: {acc:.4f}")
    print(classification_report(y_test, preds, target_names=encoder.classes_, zero_division=0))

    if acc > best_accuracy:
        best_accuracy = acc
        best_model_name = name
        best_model = model

print("\n================ SUMMARY ================")
for name, acc in sorted(results.items(), key=lambda x: -x[1]):
    print(f"{name:<25}{acc:.4f}")
print(f"\nBest model: {best_model_name} ({best_accuracy:.4f} accuracy)")

# ---------------------------------------------------------------------
# 6. Persist best model + scaler + label encoder
# ---------------------------------------------------------------------
with open(os.path.join(BASE_DIR, "crop_model.pkl"), "wb") as f:
    pickle.dump(best_model, f)

with open(os.path.join(BASE_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)

with open(os.path.join(BASE_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(encoder, f)

with open(os.path.join(BASE_DIR, "best_model_info.txt"), "w") as f:
    f.write(f"Best model: {best_model_name}\nAccuracy: {best_accuracy:.4f}\n")

print("\nSaved: crop_model.pkl, scaler.pkl, label_encoder.pkl")

"""
OptiCrop - Analysis & Chart Generation Script
-----------------------------------------------
Generates:
  1. static/charts/npk_by_crop.png        - avg N, P, K per crop
  2. static/charts/correlation_heatmap.png - feature correlation heatmap
  3. static/charts/rainfall_temp.png       - rainfall vs temperature scatter
  4. static/charts/kmeans_clusters.png     - PCA-reduced K-Means cluster plot
  5. model/crop_stats.pkl                  - dict of {crop: {N, P, K, ...avg}}
  6. model/cluster_summary.pkl             - which crops fall in which K-Means cluster

Run once (or whenever the dataset changes):
    python model/analysis.py
"""

import os
import pickle
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "dataset", "Crop_recommendation.csv")
CHART_DIR = os.path.join(BASE_DIR, "..", "static", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_style("whitegrid")
GREEN = "#2E7D32"

df = pd.read_csv(DATA_PATH)
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

# ---------------------------------------------------------------------
# 1. Average N, P, K per crop (bar chart)
# ---------------------------------------------------------------------
npk_means = df.groupby("label")[["N", "P", "K"]].mean().sort_values("N")
fig, ax = plt.subplots(figsize=(11, 7))
npk_means.plot(kind="barh", ax=ax, color=["#66BB6A", "#FFA726", "#42A5F5"])
ax.set_xlabel("Average value")
ax.set_ylabel("")
ax.set_title("Average Nitrogen, Phosphorous & Potassium Needs by Crop", fontsize=13, weight="bold")
ax.legend(["Nitrogen (N)", "Phosphorous (P)", "Potassium (K)"], loc="lower right")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "npk_by_crop.png"), dpi=110)
plt.close()

# ---------------------------------------------------------------------
# 2. Correlation heatmap
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7, 6))
sns.heatmap(df[FEATURES].corr(), annot=True, fmt=".2f", cmap="Greens", ax=ax, cbar=True)
ax.set_title("Feature Correlation Heatmap", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "correlation_heatmap.png"), dpi=110)
plt.close()

# ---------------------------------------------------------------------
# 3. Rainfall vs Temperature scatter (colored by a subset of crops for readability)
# ---------------------------------------------------------------------
highlight_crops = ["rice", "coffee", "watermelon", "chickpea", "cotton", "jute"]
subset = df[df["label"].isin(highlight_crops)]
fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=subset, x="temperature", y="rainfall", hue="label", palette="Set2", s=45, ax=ax)
ax.set_title("Rainfall vs Temperature (selected crops)", fontsize=13, weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "rainfall_temp.png"), dpi=110)
plt.close()

# ---------------------------------------------------------------------
# 4. K-Means clustering + PCA visualization (Scenario 3 - research insight)
# ---------------------------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df[FEATURES])

k = 6
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
df["cluster"] = clusters

pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)

fig, ax = plt.subplots(figsize=(9, 7))
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters, cmap="tab10", s=18, alpha=0.75)
ax.set_title(f"K-Means Clustering of Crops (k={k}), PCA-reduced", fontsize=13, weight="bold")
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
legend1 = ax.legend(*scatter.legend_elements(), title="Cluster", loc="best")
ax.add_artist(legend1)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "kmeans_clusters.png"), dpi=110)
plt.close()

# Which crops dominate each cluster
cluster_summary = {}
for c in sorted(df["cluster"].unique()):
    crops_in_cluster = df[df["cluster"] == c]["label"].value_counts().head(5)
    cluster_summary[int(c)] = list(crops_in_cluster.index)

# ---------------------------------------------------------------------
# 5. Per-crop average stats (for fertilizer recommendation module)
# ---------------------------------------------------------------------
crop_stats = df.groupby("label")[FEATURES].mean().round(1).to_dict(orient="index")

with open(os.path.join(BASE_DIR, "crop_stats.pkl"), "wb") as f:
    pickle.dump(crop_stats, f)

with open(os.path.join(BASE_DIR, "cluster_summary.pkl"), "wb") as f:
    pickle.dump(cluster_summary, f)

# ---------------------------------------------------------------------
# 6. Global feature min/max ranges (used for soil health score normalization)
# ---------------------------------------------------------------------
feature_ranges = {feat: (float(df[feat].min()), float(df[feat].max())) for feat in FEATURES}
with open(os.path.join(BASE_DIR, "feature_ranges.pkl"), "wb") as f:
    pickle.dump(feature_ranges, f)

print("Charts saved to static/charts/")
print("crop_stats.pkl and cluster_summary.pkl saved to model/")
print("\nCluster summary (top crops per cluster):")
for c, crops in cluster_summary.items():
    print(f"  Cluster {c}: {', '.join(crops)}")

# -*- coding: utf-8 -*-
"""ml project random forest

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hwi8tcMFI2Bi49yTkhWGz2f-lU7br0qU
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1) Load your CSV (with sample_id, timestamp, amplitude_mean, amplitude_std, phase_mean, phase_std, label) ---
df = pd.read_csv('/content/wi-fi_csi_motion_dataset_refined.csv')

# --- 2) Build X_seq and y_labels arrays ---
groups = df.groupby('sample_id')
X_seq, y_labels = [], []
for _, g in groups:
    g = g.sort_values('timestamp')
    X_seq.append(g[['amplitude_mean','amplitude_std','phase_mean','phase_std']].values)
    y_labels.append(g['label'].iloc[0])
X_seq = np.array(X_seq)      # shape (300, 20, 4)
y_labels = np.array(y_labels)

# --- 3) Encode labels once ---
le = LabelEncoder()
y_enc = le.fit_transform(y_labels)  # ints 0–14

# --- 4) Augmentation: sliding windows + jittering ---
def sliding_windows(X, y, win_size=10, step=2):
    Xw, yw = [], []
    for seq, lbl in zip(X, y):
        for start in range(0, seq.shape[0] - win_size + 1, step):
            Xw.append(seq[start:start+win_size])
            yw.append(lbl)
    return np.array(Xw), np.array(yw)

def jitter(data, sigma=0.02):
    return data + np.random.normal(0, sigma, data.shape)

# create windows
X_win, y_win = sliding_windows(X_seq, y_enc, win_size=10, step=2)
# jitter each window once (double your data)
X_jit = jitter(X_win)
X_aug = np.vstack([X_win, X_jit])
y_aug = np.concatenate([y_win, y_win])

print(f"Augmented dataset shape: X={X_aug.shape}, y={y_aug.shape}")
# Expect roughly (300 * ((20-10)/2+1) * 2) ≈ (300*6*2)=3600 samples

# --- 5) Flatten windows for RandomForest ---
X_flat = X_aug.reshape(X_aug.shape[0], -1)  # (n_samples, 10*4=40 features)

# --- 6) Scale features ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_flat)

# --- 7) Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_aug, test_size=0.2, stratify=y_aug, random_state=42
)

# --- 8) Train a tuned Random Forest ---
clf = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
clf.fit(X_train, y_train)

# --- 9) Evaluate ---
y_pred = clf.predict(X_test)
print(f"\n Accuracy: {accuracy_score(y_test, y_pred):.2f}\n")
print(" Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# --- 10) Plot confusion matrix ---
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=le.classes_,
            yticklabels=le.classes_,
            cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix after Augmentation")
plt.show()

!pip install gradio

joblib.dump(clf, 'rf_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(le, 'label_encoder.pkl')

import gradio as gr
import numpy as np
import joblib

# Load model and tools
clf = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")
le = joblib.load("label_encoder.pkl")

# Predict function
def predict_position(amplitude_mean, amplitude_std, phase_mean, phase_std):
    input_seq = np.array([[amplitude_mean, amplitude_std, phase_mean, phase_std]] * 10).reshape(1, -1)
    input_scaled = scaler.transform(input_seq)
    pred = clf.predict(input_scaled)[0]
    label = le.inverse_transform([pred])[0]
    return f"🎯 Predicted Position: {label}"

# Interface
with gr.Blocks(css="""
body {
    background: linear-gradient(to right, #9b59b6, #8e44ad);
    font-family: 'Segoe UI', sans-serif;
}
#main {
    max-width: 720px;
    margin: 40px auto;
    padding: 30px;
    background: #ffffffee;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
#main_title {
    text-align: center;
    font-size: 3.8em;
    font-weight: 900;
    background: linear-gradient(90deg, #a855f7, #d8b4fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 6px #b06aed);
    margin-bottom: 30px;
    font-family: 'Segoe UI Black', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

input[type=number] {
    background: #f5f0ff !important;
    border: 2px solid #b57edc !important;
    padding: 12px;
    border-radius: 12px;
    font-size: 1em;
}
textarea, input, .gr-box {
    box-shadow: 0 6px 14px rgba(155,89,182,0.1) !important;
}
#prediction {
    font-size: 1.4em;
    font-weight: bold;
    color: #4a0066;
    background-color: #f3e8ff;
    border: 2px solid #c084fc;
    padding: 16px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(155,89,182,0.25);
}
img {
    display: block;
    margin: 0 auto 20px auto;
    max-height: 120px;
    border-radius: 14px;
    border: 2px solid #d1b3ff;
}
button {
    background-color: #a855f7 !important;
    color: white !important;
    padding: 14px 30px;
    font-size: 1.1em;
    font-weight: bold;
    border-radius: 14px;
    margin-top: 10px;
    transition: background 0.3s ease;
}
button:hover {
    background-color: #9333ea !important;
}
""") as demo:

    with gr.Column(elem_id="main"):
        gr.Markdown(" **CSI Motion Classifier**", elem_id="main_title")

        gr.Image(value="/content/1043-signal-streams.gif", interactive=False)

        with gr.Row():
            amplitude_mean = gr.Number(label="📊 Amplitude Mean")
            amplitude_std = gr.Number(label="📉 Amplitude Std")

        with gr.Row():
            phase_mean = gr.Number(label="🌐 Phase Mean")
            phase_std = gr.Number(label="🔄 Phase Std")

        predict_btn = gr.Button("🚀 Predict")
        output = gr.Text(label="Result", elem_id="prediction")

        predict_btn.click(
            fn=predict_position,
            inputs=[amplitude_mean, amplitude_std, phase_mean, phase_std],
            outputs=output
        )

demo.launch()

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import random

# --- 1) Load your CSV ---
df = pd.read_csv('/content/wi-fi_csi_motion_dataset_refined.csv')

# --- 2) Build sequences ---
groups = df.groupby('sample_id')
X_seq, y_labels = [], []
for _, g in groups:
    g = g.sort_values('timestamp')
    X_seq.append(g[['amplitude_mean','amplitude_std','phase_mean','phase_std']].values)
    y_labels.append(g['label'].iloc[0])
X_seq = np.array(X_seq)      # shape (300, 20, 4)
y_labels = np.array(y_labels)

# --- 3) Encode labels ---
le = LabelEncoder()
y_enc = le.fit_transform(y_labels)

# --- 4) Augmentation ---
def sliding_windows(X, y, win_size=10, step=2):
    Xw, yw = [], []
    for seq, lbl in zip(X, y):
        for start in range(0, seq.shape[0] - win_size + 1, step):
            Xw.append(seq[start:start+win_size])
            yw.append(lbl)
    return np.array(Xw), np.array(yw)

def jitter(data, sigma=0.02):
    return data + np.random.normal(0, sigma, data.shape)

X_win, y_win = sliding_windows(X_seq, y_enc, win_size=10, step=2)
X_jit = jitter(X_win)
X_aug = np.vstack([X_win, X_jit])
y_aug = np.concatenate([y_win, y_win])

print(f"Augmented dataset shape: X={X_aug.shape}, y={y_aug.shape}")

# --- 5) Flatten ---
X_flat = X_aug.reshape(X_aug.shape[0], -1)

# --- 6) Scaling ---
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_flat)

# --- 7) Train/test split ---
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y_aug, test_size=0.2, stratify=y_aug, random_state=42
)

# --- 8) Model training ---
clf = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
clf.fit(X_train, y_train)

# --- 9) Evaluation ---
y_pred = clf.predict(X_test)
print(f"\n🔍 Accuracy: {accuracy_score(y_test, y_pred):.2f}\n")
print("📊 Classification Report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))

# --- 10) Confusion Matrix ---
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=le.classes_,
            yticklabels=le.classes_,
            cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix after Augmentation")
plt.show()

# --- 11) Test predictions on 2 new samples ---
print("\n🎯 Predicting on 2 random test samples:")
sample_indices = random.sample(range(len(X_test)), 2)

for idx in sample_indices:
    sample = X_test[idx].reshape(1, -1)
    true_label = le.inverse_transform([y_test[idx]])[0]
    predicted_label = le.inverse_transform(clf.predict(sample))[0]
    print(f"Sample {idx} ➤ True: {true_label}, Predicted: {predicted_label}")










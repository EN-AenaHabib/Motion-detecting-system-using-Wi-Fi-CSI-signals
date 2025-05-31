

---

# 📡 CSI Motion Classifier

**Detect Human Motion Using WiFi Signals — No Cameras. Just Waves.**

---

## 🚀 Overview

This project explores the innovative use of **WiFi Channel State Information (CSI)** to detect human motion **without cameras or sensors** — just by analyzing subtle changes in WiFi signal data. It's a privacy-preserving, cost-effective approach to motion detection that opens the door to applications in **smart homes, security, and health monitoring**.

We use a **Random Forest Classifier** trained on a refined CSI dataset to accurately classify different motion positions based on amplitude and phase data.

---

## 💡 Key Features

* 🔍 Motion classification using CSI features: `amplitude_mean`, `amplitude_std`, `phase_mean`, `phase_std`
* 🧠 Trained and tested multiple ML models — **Random Forest** gave the best accuracy
* 🧪 Data augmentation via **sliding windows + jittering**
* 📊 Model evaluation with confusion matrix & classification report
* 🌐 Beautiful, interactive **Gradio interface**
* 🖼️ Live GIF preview embedded in the UI
* 🧪 Built and run entirely on **Google Colab**

---

## 🎯 Live Prediction Demo (Gradio)

Input CSI features manually and get **real-time prediction** of the motion label:

<img src="/content/1043-signal-streams.gif" width="600">

Try the interface in Google Colab after uploading:

* Your **WiFi CSI dataset** (`wi-fi_csi_motion_dataset_refined.csv`)
* The preview **GIF** for UI enhancement

---

## 🔧 How It Works

1. **Load CSI dataset** grouped by `sample_id`
2. **Extract sequences** of CSI stats (20 timestamps per sample)
3. **Augment data** using sliding windows (win=10, step=2) + noise
4. **Flatten & scale** data for ML model
5. **Train Random Forest** with balanced class weights
6. **Evaluate** using accuracy, precision, and confusion matrix
7. **Deploy with Gradio** for user-friendly prediction interface

---

## 🛠️ Still in Progress

We’re actively working on the **real-time CSI signal capture** from a router, to move beyond static datasets and build a complete **end-to-end motion detection system.**

---

## 🧪 Requirements

* Python (Colab pre-installed)
* pandas, numpy, sklearn, seaborn, matplotlib
* Gradio for interactive UI
* joblib for model saving/loading

---

## 🧠 Model Performance

| Model         | Accuracy    |
| ------------- | ----------- |
| Random Forest | ✅ Best      |
| SVM           | ⚠️ Moderate |
| KNN           | ⚠️ Lower    |
| Logistic Reg. | ⚠️ Lower    |

---

## 📁 Files

* `rf_model.pkl` – Trained Random Forest model
* `scaler.pkl` – StandardScaler for input features
* `label_encoder.pkl` – Encoded motion labels
* `Gradio UI` – Intuitive web-based predictor

---

## 📌 Run It Yourself

1. Open in **Google Colab**
2. Upload:

   * Dataset CSV (`wi-fi_csi_motion_dataset_refined.csv`)
   * Preview GIF (`1043-signal-streams.gif`)
3. Run all cells
4. Launch Gradio app and test your motion input!

---

## 💬 Future Goals

* ✅ Dataset-based prediction
* 🔄 Real-time WiFi signal capture using routers
* 📉 Compare deep learning (e.g., LSTM) with classical models
* 📱 Mobile interface (possible Flutter/Python bridge)

---

## 👨‍💻 Team

This project is a semester research work, currently under development and experimentation for future real-world deployment.

---



# 🏥 PathoDx — Pathology Disease Predictor
### Multi-Output Decision Tree Clinical Decision Support System | DIU FYDP

---

## 📁 Project Structure

```
Pathology_Disease_Prediction/
│
├── app.py                      ← Main Flask application controller
├── train_model.py              ← Model training script (Decision Tree)
├── requirements.txt            ← Python dependencies
├── README.md                   ← Project documentation
│
├── project/
│   ├── Final_Pathology_ML.ipynb← Research, EDA, and model evaluation notebook
│   └── data/
│       └── pathology_dataset.csv ← Clinical dataset (1,210 patient records)
│
├── model/
│   ├── decision_tree_model.pkl ← Trained Decision Tree MultiOutput model (Best)
│   └── scaler.pkl              ← StandardScaler fitted on clinical features
│
├── static/
│   ├── css/
│   │   └── style.css           ← Modern medical UI stylesheet
│   └── js/
│       └── main.js             ← Client-side AJAX submission & UI rendering
│
└── templates/
    ├── index.html              ← Main clinical diagnosis interface
    └── about.html              ← 5-Model performance comparison & benchmark page
```

---

## 🚀 How to Run (Step by Step)

### Step 1 — Install Python Packages
```bash
pip install -r requirements.txt
```

### Step 2 — Train or Verify Model Files
```bash
python train_model.py
```
This trains the best Decision Tree MultiOutput Classifier and generates:
- `model/decision_tree_model.pkl`
- `model/scaler.pkl`

### Step 3 — Run the Flask Web Application
```bash
python app.py
```

### Step 4 — Open in Web Browser
Navigate to:
```
http://127.0.0.1:5000
```

---

## 🤖 Model Performance & Evaluation

Extensively evaluated across 5 machine learning algorithms on 1,210 clinical records in `Final_Pathology_ML.ipynb`:

| Metric | Decision Tree (Best Model) |
|---|---|
| **Algorithm** | Decision Tree Classifier (`max_depth=3`, `min_samples_leaf=15`) |
| **Architecture** | MultiOutputClassifier (8 simultaneous outputs) |
| **Dataset** | 1,210 Clinical Records (`pathology_dataset.csv`) |
| **Accuracy** | **97.11%** Exact Match |
| **Precision** | **99.41%** (Weighted) |
| **Recall** | **97.94%** (Weighted) |
| **F1 Score** | **98.57%** (Weighted) |

---

## 🦠 Pathology Conditions Detected

1. **Anemia** (Low Hemoglobin)
2. **Prediabetes** (Impaired Glucose)
3. **Diabetes** (High RBS)
4. **Kidney Problem** (Elevated Creatinine)
5. **Inflammation** (Elevated ESR)
6. **Hepatitis B** (HBsAg Reactive)
7. **Leukopenia** (Low WBC)
8. **Leukocytosis** (High WBC)

---

## 📥 Laboratory Input Features

| Feature | Unit | Normal Reference Range |
|---|---|---|
| **Sex** | Categorical | Male (1) / Female (0) |
| **Hemoglobin** | Hb % | Male: 13–17, Female: 12–15 |
| **RBS** | mmol/L | Normal: < 7.8 |
| **Creatinine** | mg/dL | 0.6–1.3 |
| **ESR** | mm/hr | 0–20 |
| **HBsAg** | Categorical | Negative (0) / Positive (1) |
| **WBC** | cells/μL | 4,000–11,000 |

---

## 👨‍💻 Project Information

- **Md. Naimul Islam** (ID: 0242220005101086)

**Supervisor:** Mr. Mehadi Hasan (Lecturer, Department of CSE, Daffodil International University)

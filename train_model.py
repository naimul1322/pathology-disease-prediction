import sys
import types

# Windows Smart App Control compatibility fix for Python 3.14 / scikit-learn
if 'sklearn.metrics._pairwise_distances_reduction._radius_neighbors_classmode' not in sys.modules:
    dummy_rn = types.ModuleType('sklearn.metrics._pairwise_distances_reduction._radius_neighbors_classmode')
    dummy_rn.RadiusNeighborsClassMode64 = None
    dummy_rn.RadiusNeighborsClassMode32 = None
    sys.modules['sklearn.metrics._pairwise_distances_reduction._radius_neighbors_classmode'] = dummy_rn

import os
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.multioutput import MultiOutputClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 7 laboratory test features identified from Final_Pathology_ML.ipynb
FEATURES = [
    'Sex',
    'Hemoglobin (Hb %)',
    'RBS (mmol/L)',
    'Creatinine (mg/dc)',
    'ESR(mm/hr)',
    'HBsAg',
    'WBC (White Blood Cell)'
]

# 8 target pathology diseases for multi-output prediction
DISEASE_LABELS = [
    'Anemia',
    'Prediabetes',
    'Diabetes',
    'Kidney Problem',
    'Inflammation',
    'Hepatitis B',
    'Leukopenia',
    'Leukocytosis'
]


def train_and_save():
    
    # 1. Locate the dataset
    data_path = os.path.join('project', 'data', 'pathology_dataset.csv')
    if not os.path.exists(data_path):
        data_path = 'pathology_dataset.csv'

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Pathology dataset could not be found at: {data_path}")

    print(f"[1/5] Loading clinical pathology dataset from {data_path}...")
    df = pd.read_csv(data_path)
    print(f"      Loaded {len(df)} patient records.")

    # 2. Encode categorical features:
    # Sex: Female -> 0, Male -> 1
    # HBsAg: Negative -> 0, Positive -> 1
    df['Sex'] = df['Sex'].map({'Female': 0, 'Male': 1}).fillna(0).astype(int)
    df['HBsAg'] = df['HBsAg'].map({'Negative': 0, 'Positive': 1}).fillna(0).astype(int)

    # 3. Create binary columns for each target disease
    for disease in DISEASE_LABELS:
        df[disease] = df['Diseases'].apply(lambda d: 1 if disease in str(d) else 0)

    X = df[FEATURES].values
    y = df[DISEASE_LABELS].values

    # 4. Split dataset into 80% training and 20% test sets (random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 5. Fit StandardScaler on training features
    print("[2/5] Standardizing clinical features using StandardScaler...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 6. Train Decision Tree MultiOutputClassifier (Best Model from notebook)
    print("[3/5] Training Decision Tree Classifier (max_depth=3, min_samples_leaf=15)...")
    base_tree = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=15,
        random_state=42
    )
    dt_model = MultiOutputClassifier(base_tree)
    dt_model.fit(X_train_scaled, y_train)

    # 7. Evaluate on the hold-out test set
    y_pred = dt_model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print("[4/5] Decision Tree Model Evaluation:")
    print(f"      - Exact Match Accuracy: {acc * 100:.2f}%")
    print(f"      - Precision (Weighted): {prec * 100:.2f}%")
    print(f"      - Recall (Weighted):    {rec * 100:.2f}%")
    print(f"      - F1 Score (Weighted):  {f1 * 100:.2f}%")

    # 8. Save model and scaler artifacts
    os.makedirs('model', exist_ok=True)
    model_path = os.path.join('model', 'decision_tree_model.pkl')
    scaler_path = os.path.join('model', 'scaler.pkl')

    with open(model_path, 'wb') as f_model:
        pickle.dump(dt_model, f_model)

    with open(scaler_path, 'wb') as f_scaler:
        pickle.dump(scaler, f_scaler)

    print(f"[5/5] Best model successfully saved:")
    print(f"      -> {model_path}")
    print(f"      -> {scaler_path}")


if __name__ == '__main__':
    train_and_save()

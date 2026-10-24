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
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base directories and model file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'decision_tree_model.pkl')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.pkl')

# Automatically train and generate Decision Tree model if files are not found
if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    from train_model import train_and_save
    train_and_save()

# Load the trained MultiOutput Decision Tree model and StandardScaler
with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

with open(SCALER_PATH, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

# 8 pathology diseases classified simultaneously (MultiOutput setup)
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

# Clinical treatments and lifestyle recommendations per condition
TREATMENTS = {

    'Anemia': {
        'icon': '🩸',
        'color': '#ef4444',
        'description': 'Low hemoglobin level detected.',
        'medicines': [
            'Iron supplements — as prescribed by doctor',
            'Vitamin B12 — if recommended by doctor',
            'Folic Acid — if recommended by doctor'
        ],
        'advice': [
            'Eat iron-rich foods like spinach, lentils, beans and meat',
            'Avoid tea or coffee right after meals',
            'Repeat a blood test in about 4 weeks'
        ]
    },

    'Prediabetes': {
        'icon': '🍬',
        'color': '#f59e0b',
        'description': 'Blood sugar is higher than normal.',
        'medicines': [
            'Metformin — only if prescribed by doctor',
            'Vitamin D3 — if recommended by doctor'
        ],
        'advice': [
            'Reduce sugar and processed foods',
            'Exercise or walk for at least 30 minutes daily',
            'Check blood sugar regularly'
        ]
    },

    'Diabetes': {
        'icon': '💉',
        'color': '#ea580c',
        'description': 'Blood sugar is significantly higher than normal.',
        'medicines': [
            'Metformin — only if prescribed by doctor',
            'Insulin — only as directed by doctor',
            'Other diabetes medicines — as prescribed'
        ],
        'advice': [
            'Follow a low-sugar, healthy diet',
            'Check blood sugar regularly',
            'Test HbA1c every 3 months as advised'
        ]
    },

    'Kidney Problem': {
        'icon': '🫘',
        'color': '#b45309',
        'description': 'Creatinine level may indicate a kidney problem.',
        'medicines': [
            'ACE Inhibitors / ARBs — only if prescribed',
            'Phosphate binders — only if prescribed'
        ],
        'advice': [
            'Reduce salt and follow a healthy diet',
            'Drink enough water unless doctor advises otherwise',
            'Avoid Ibuprofen and similar painkillers without advice',
            'Consult a kidney specialist if needed'
        ]
    },

    'Inflammation': {
        'icon': '🔬',
        'color': '#8b5cf6',
        'description': 'High ESR may indicate inflammation.',
        'medicines': [
            'Ibuprofen / Naproxen — only if recommended',
            'Corticosteroids — only if prescribed',
            'Antibiotics — only for confirmed infection'
        ],
        'advice': [
            'Get enough rest and sleep',
            'Eat healthy food with fruits and vegetables',
            'Repeat ESR test if advised',
            'Consult a doctor to find the cause'
        ]
    },

    'Hepatitis B': {
        'icon': '🦠',
        'color': '#0284c7',
        'description': 'Hepatitis B infection was detected.',
        'medicines': [
            'Tenofovir or Entecavir — only if prescribed',
            'Interferon — only if recommended by specialist'
        ],
        'advice': [
            'Avoid alcohol completely',
            'Check liver tests regularly as advised',
            'Vaccinate family members and close contacts',
            'Consult a liver specialist'
        ]
    },

    'Leukopenia': {
        'icon': '🩺',
        'color': '#0284c7',
        'description': 'White blood cell count is lower than normal.',
        'medicines': [
            'G-CSF — only for severe cases under doctor supervision',
            'Antibiotics — only if infection is confirmed'
        ],
        'advice': [
            'Avoid crowded places when possible',
            'Wash hands regularly and keep clean',
            'See a doctor if you develop fever or chills'
        ]
    },

    'Leukocytosis': {
        'icon': '⚗️',
        'color': '#059669',
        'description': 'White blood cell count is higher than normal.',
        'medicines': [
            'Antibiotics — only for confirmed bacterial infection',
            'Anti-inflammatory medicine — if recommended by doctor'
        ],
        'advice': [
            'Find the possible cause of the high WBC count',
            'Repeat CBC test if advised',
            'Follow the doctor’s treatment plan'
        ]
    },

    'Normal': {
        'icon': '✅',
        'color': '#16a34a',
        'description': 'Your test results are within the normal range.',
        'medicines': [
            'No medication required'
        ],
        'advice': [
            'Eat a balanced diet and stay active',
            'Drink enough water and sleep 7–8 hours',
            'Have a routine health checkup'
        ]
    }
}


@app.route('/')
def home():
    """Renders the primary patient clinical input form."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Receives patient lab values, scales features with StandardScaler,
    predicts 8 conditions simultaneously using the best Decision Tree Classifier,
    and returns detected conditions with clinical recommendations.
    """
    try:
        # Extract and parse input parameters from the request
        sex = int(request.form.get('sex', 0))
        hb = float(request.form.get('hemoglobin', 0))
        rbs = float(request.form.get('rbs', 0))
        creatinine = float(request.form.get('creatinine', 0))
        esr = float(request.form.get('esr', 0))
        hbsag = int(request.form.get('hbsag', 0))
        wbc = float(request.form.get('wbc', 0))

        # Basic range and positivity validation
        if hb <= 0 or rbs <= 0 or creatinine <= 0 or esr < 0 or wbc <= 0:
            return jsonify({
                'success': False,
                'error': 'Please enter valid positive values for all laboratory fields.'
            }), 400

        # Construct input array in the exact order of model training:
        # ['Sex', 'Hemoglobin (Hb %)', 'RBS (mmol/L)', 'Creatinine (mg/dc)', 'ESR(mm/hr)', 'HBsAg', 'WBC (White Blood Cell)']
        features = np.array([[sex, hb, rbs, creatinine, esr, hbsag, wbc]])
        scaled_features = scaler.transform(features)

        # Predict using Decision Tree MultiOutputClassifier
        raw_prediction = model.predict(scaled_features)[0]

        # Extract detected pathology conditions
        detected_diseases = [
            DISEASE_LABELS[i]
            for i, val in enumerate(raw_prediction)
            if val == 1
        ]

        # Flag as normal if no conditions were triggered
        is_normal = len(detected_diseases) == 0
        if is_normal:
            detected_diseases = ['Normal']

        # Retrieve clinical treatments and advice
        treatment_info = [TREATMENTS[disease] for disease in detected_diseases]

        return jsonify({
            'success': True,
            'diseases': detected_diseases,
            'treatments': treatment_info,
            'count': 0 if is_normal else len(detected_diseases),
            'is_normal': is_normal
        })

    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid numeric input format. Please check all entries.'
        }), 400
    except Exception as err:
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(err)}'
        }), 500


@app.route('/about')
def about():
    """Renders the model architecture and performance evaluation page."""
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True,port=5000)

"""
Run script for Pathology Disease Prediction System.
"""
from app import app

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Pathology Disease Prediction Web App is Running!")
    print(" Local URL: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host='127.0.0.1', port=5000, debug=True)

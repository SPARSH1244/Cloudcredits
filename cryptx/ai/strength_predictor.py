import re
import joblib
import os

model_path = os.path.join(os.path.dirname(__file__), "password_model.pkl")
model = joblib.load(model_path)

def extract_features(password):
    length = len(password)
    has_mix = bool(re.search(r'[a-z]', password)) and bool(re.search(r'[A-Z]', password))
    has_symbols = len(re.findall(r'[^a-zA-Z0-9]', password))

    # Encode into simple feature list
    return [[
        length,
        int(has_mix),
        int(has_symbols > 0) + int(has_symbols > 3)
    ]]

def predict_strength(password):
    features = extract_features(password)
    prediction = model.predict(features)[0]

    levels = [
        ("Very Weak", "Too short or obvious"),
        ("Weak", "Consider using mixed characters"),
        ("Moderate", "Try adding more special symbols"),
        ("Strong", "Good, but can be better"),
        ("Very Strong", "Excellent password!")
    ]

    return levels[prediction]

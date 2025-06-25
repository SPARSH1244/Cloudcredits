import joblib
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Fake training dataset
X = [
    [5, 0, 1],    # weak, short, numbers only
    [8, 1, 0],    # weak, simple lowercase
    [12, 1, 1],   # medium, mix
    [16, 1, 2],   # strong, mix + special
    [20, 1, 3],   # very strong
]

y = [0, 1, 2, 3, 4]  # 0=Very Weak, 4=Very Strong

model = RandomForestClassifier(n_estimators=20)
model.fit(X, y)

joblib.dump(model, "ai/password_model.pkl")
print("Model trained and saved!")

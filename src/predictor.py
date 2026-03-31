# src/predictor.py — Real-time prediction engine

import joblib
import pandas as pd
from config import MODEL_PATH, LABEL_BUY, LABEL_SELL, LABEL_NONE

FEATURES = ["mdr", "volume_delta", "spread", "trend", "aggression", "trade_speed"]

class Predictor:
    def __init__(self):
        print("🔮 Loading trained model...")
        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: dict) -> str:
        """
        Input : feature dictionary from feature_engineering.py
        Output: "BUY_FAST", "SELL_FAST", or "NO_MOVE"
        """
        row = pd.DataFrame([features])[FEATURES]
        prediction = self.model.predict(row)[0]
        return prediction
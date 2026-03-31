# src/model_trainer.py — Trains the ML classification model

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from config import DATA_PATH, MODEL_PATH

FEATURES = ["mdr", "volume_delta", "spread", "trend", "aggression", "trade_speed"]

def train_model():
    print("📂 Loading data...")
    df = pd.read_csv(DATA_PATH)
    df.dropna(inplace=True)

    X = df[FEATURES]
    y = df["label"]

    # Split into train and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("🤖 Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,    # 100 decision trees
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate accuracy
    y_pred = model.predict(X_test)
    print("\n📊 Model Performance:")
    print(classification_report(y_test, y_pred))

    # Save model to disk
    joblib.dump(model, MODEL_PATH)
    print(f"\n✅ Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
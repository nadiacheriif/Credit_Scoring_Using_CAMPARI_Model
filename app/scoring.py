import joblib
import numpy as np
from app.preprocessing import transform_data
from app.validation import validate_input

model = joblib.load("artifacts/model.pkl")
config = joblib.load("artifacts/scoring_config.pkl")


def calculate_score(probability):
    odds = (1 - probability) / probability
    score = config["BASE_SCORE"] - config["PDO"] * np.log(odds) / np.log(2)
    return round(score)


def score_client(input_data):

    # =============================
    # 1️⃣ Validate input
    # =============================
    errors = validate_input(input_data)
    if errors:
        return {"errors": errors}

    # =============================
    # 2️⃣ Transform
    # =============================
    X = transform_data(input_data)

    # =============================
    # 3️⃣ Predict
    # =============================
    probability = model.predict_proba(X)[0][1]
    score = calculate_score(probability)

    # =============================
    # 4️⃣ Decision logic
    # =============================
    threshold = config["best_threshold"]
    buffer = config["buffer"]

    if probability < threshold - buffer:
        decision = "APPROVE"
    elif probability > threshold + buffer:
        decision = "REJECT"
    else:
        decision = "REVIEW"

    return {
        "credit_score": score,
        "probability_default": probability,
        "decision": decision
    }

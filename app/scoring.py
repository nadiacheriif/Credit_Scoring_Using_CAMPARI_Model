import numpy as np
import pandas as pd
from app.config import model, BASE_SCORE, PDO, BEST_THRESHOLD, BUFFER
from app.preprocessing import transform_data
from app.data_validation import validate_input

factor = PDO / np.log(2)

def compute_score(prob):
    prob = np.clip(prob, 1e-6, 1 - 1e-6)
    odds = prob / (1 - prob)
    log_odds = np.log(odds)
    return round(BASE_SCORE + factor * log_odds, 0)

def make_decision(prob):

    if prob >= BEST_THRESHOLD + BUFFER:
        return "Approve"
    elif prob <= BEST_THRESHOLD - BUFFER:
        return "Reject"
    else:
        return "Manual Review"

def score_client(input_dict):

    df = pd.DataFrame([input_dict])

    validate_input(df)

    X_processed = transform_data(df)

    prob = model.predict_proba(X_processed)[:, 1][0]

    score = compute_score(prob)

    decision = make_decision(prob)

    return {
        "probability_good": float(prob),
        "credit_score": score,
        "decision": decision
    }

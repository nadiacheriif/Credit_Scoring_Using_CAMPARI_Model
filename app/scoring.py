import numpy as np
from app.config import model, BEST_THRESHOLD, BUFFER, BASE_SCORE, PDO
from app.preprocessing import transform_data


def calculate_score(probability: float):

    odds = probability / (1 - probability)
    factor = PDO / np.log(2)
    offset = BASE_SCORE - factor * np.log(1)

    score = offset - factor * np.log(odds)
    return round(score, 0)


def decision_logic(probability: float):

    if probability >= BEST_THRESHOLD + BUFFER:
        return "REJECT"

    elif probability <= BEST_THRESHOLD - BUFFER:
        return "APPROVE"

    else:
        return "MANUAL REVIEW"


def score_client(input_data: dict):

    X = transform_data(input_data)

    probability = model.predict_proba(X)[0][1]

    decision = decision_logic(probability)

    score = calculate_score(probability)

    return {
        "probability_default": round(float(probability), 4),
        "credit_score": int(score),
        "decision": decision
    }

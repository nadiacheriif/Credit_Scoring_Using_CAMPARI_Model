from pathlib import Path
import joblib
import os


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS_PATH = BASE_DIR / "artifacts"


model = joblib.load(os.path.join(ARTIFACTS_PATH, "model.pkl"))
bins = joblib.load(os.path.join(ARTIFACTS_PATH, "woe_bins.pkl"))
feature_columns = joblib.load(os.path.join(ARTIFACTS_PATH, "feature_columns.pkl"))
scoring_config = joblib.load(os.path.join(ARTIFACTS_PATH, "scoring_config.pkl"))

BEST_THRESHOLD = scoring_config["best_threshold"]
BUFFER = scoring_config["buffer"]
BASE_SCORE = scoring_config["BASE_SCORE"]
PDO = scoring_config["PDO"]

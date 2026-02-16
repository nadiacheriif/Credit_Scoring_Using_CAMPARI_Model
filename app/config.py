from pathlib import Path
import joblib

# Project root (one level above app/)
BASE_DIR = Path(__file__).resolve().parent.parent

ARTIFACTS_PATH = BASE_DIR / "artifacts"

MODEL_PATH = ARTIFACTS_PATH / "model.pkl"
WOE_PATH = ARTIFACTS_PATH / "woe_bins.pkl"
CONFIG_PATH = ARTIFACTS_PATH / "config.pkl"

# Check files exist before loading
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

if not WOE_PATH.exists():
    raise FileNotFoundError(f"WOE file not found at {WOE_PATH}")

if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

model = joblib.load(MODEL_PATH)
woe = joblib.load(WOE_PATH)
config = joblib.load(CONFIG_PATH)

BASE_SCORE = config["BASE_SCORE"]
PDO = config["PDO"]
BEST_THRESHOLD = config["best_threshold"]
BUFFER = config.get("buffer", 0.05)

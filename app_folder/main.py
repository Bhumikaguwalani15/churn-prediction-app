from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
from pathlib import Path
import logging

from schemas import CustomerData, PredictionResponse, HealthResponse
from utils import preprocess_customer_data, determine_risk_level

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
scaler = None
feature_columns = None

# ✅ FIXED MODEL PATH
@app.on_event("startup")
async def load_model():
    global model, scaler, feature_columns
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
        model_path = BASE_DIR / "model_folder"

        print("📦 Loading model from:", model_path)

        model = joblib.load(model_path / "churn_model.pkl")
        scaler = joblib.load(model_path / "scaler.pkl")
        feature_columns = joblib.load(model_path / "feature_columns.pkl")

        print("✅ Model loaded successfully")

    except Exception as e:
        print("❌ Model loading error:", e)
        model = None


@app.get("/")
def root():
    return {"message": "API running"}


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        model_loaded=model is not None,
        version="1.0.0"
    )


@app.post("/predict", response_model=PredictionResponse)
def predict(customer: CustomerData):

    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        processed = preprocess_customer_data(
            customer.dict(),
            feature_columns,
            scaler
        )

        prob = model.predict_proba(processed)[0][1]
        prediction = "Churn" if prob > 0.5 else "No Churn"

        return PredictionResponse(
            prediction=prediction,
            probability=round(float(prob), 4),
            risk_level=determine_risk_level(prob)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
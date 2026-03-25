from pydantic import BaseModel

class CustomerData(BaseModel):
    tenure: float
    monthly_charges: float
    total_charges: float

class PredictionResponse(BaseModel):
    prediction: str
    probability: float
    risk_level: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
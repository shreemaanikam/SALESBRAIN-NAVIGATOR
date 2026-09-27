from fastapi import APIRouter, HTTPException
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse, ModelStatus
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.get("/models/status", response_model=ModelStatus)
def get_model_status():
    if not prediction_service.is_ready():
        return ModelStatus(available=False)
    info = prediction_service.get_model_info()
    return ModelStatus(
        available=True,
        model_name=info.get("model_name"),
        metrics=info.get("metrics"),
        features=info.get("features")
    )

@router.get("/models/metrics")
def get_model_metrics():
    if not prediction_service.is_ready():
        raise HTTPException(status_code=503, detail="Model not ready")
    return prediction_service.get_model_info().get("metrics", {})

@router.post("/predictions/profit", response_model=PredictionResponse)
def predict_profit(request: PredictionRequest):
    if not prediction_service.is_ready():
        raise HTTPException(status_code=503, detail="Model not ready")
    
    result = prediction_service.predict(request.model_dump())
    return PredictionResponse(**result)

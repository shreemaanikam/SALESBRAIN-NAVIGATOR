from fastapi import APIRouter
from backend.app.schemas.prediction import PredictionRequest
from backend.app.services.explanation_service import explanation_service

router = APIRouter()

@router.get("/explanations/global")
def get_global_explanation():
    return explanation_service.global_explanation()

@router.post("/explanations/prediction")
def get_local_explanation(request: PredictionRequest):
    return explanation_service.local_explanation(request.model_dump())

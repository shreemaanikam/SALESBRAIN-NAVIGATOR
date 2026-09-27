from fastapi import APIRouter, HTTPException
from backend.app.schemas.scenario import SimulationRequest, SimulationResponse
from backend.app.services.scenario_service import scenario_service

router = APIRouter()

@router.post("/simulate", response_model=SimulationResponse)
def simulate_scenario(request: SimulationRequest):
    try:
        res = scenario_service.simulate(
            request.baseline.model_dump(), 
            request.scenario.model_dump()
        )
        return SimulationResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

from fastapi import Request
from fastapi.responses import JSONResponse

class DatasetNotFoundError(Exception):
    pass

class DataValidationError(Exception):
    pass

class ModelNotReadyError(Exception):
    pass

class PredictionError(Exception):
    pass

async def global_exception_handler(request: Request, exc: Exception):
    status_code = 500
    error = "InternalServerError"
    
    if isinstance(exc, DatasetNotFoundError):
        status_code = 404
        error = "DatasetNotFoundError"
    elif isinstance(exc, DataValidationError):
        status_code = 400
        error = "DataValidationError"
    elif isinstance(exc, ModelNotReadyError):
        status_code = 503
        error = "ModelNotReadyError"
    elif isinstance(exc, PredictionError):
        status_code = 500
        error = "PredictionError"

    return JSONResponse(
        status_code=status_code,
        content={"error": error, "detail": str(exc), "status_code": status_code}
    )

import os
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import json

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

# AUTH_MODE can be "local" or "firebase"


# In local mode, if no token is provided, fallback to a default dev user
# But if it's production and missing, it should fail


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Returns the user_id of the authenticated user.
    """
    AUTH_MODE = os.getenv("AUTH_MODE", "local")
    IS_PRODUCTION = os.getenv("RENDER", "false") == "true" or os.getenv("ENVIRONMENT") == "production"
    if AUTH_MODE == "local":
        if IS_PRODUCTION:
            logger.error("Security Risk: Local auth mode is enabled in production!")
            raise HTTPException(status_code=500, detail="Invalid server configuration.")
            
        # For local testing without a frontend token
        if not credentials:
            return "local_dev_user"
        return credentials.credentials

    # Firebase Authentication Mode
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required.")
        
    token = credentials.credentials
    try:
        from firebase_admin import auth
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

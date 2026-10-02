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
    IS_PRODUCTION = os.getenv("VERCEL_ENV") == "production" or os.getenv("RENDER", "false") == "true" or os.getenv("ENVIRONMENT") == "production"
    AUTH_MODE = os.getenv("AUTH_MODE", "firebase" if IS_PRODUCTION else "local")

    if AUTH_MODE == "local":

            
        # For local testing without a frontend token
        if not credentials:
            return "local_dev_user"
            
        token = credentials.credentials
        # If token is a JWT, extract the user_id or sub to avoid massive file names
        if token.startswith("eyJ") and token.count(".") == 2:
            import base64
            import json
            try:
                payload = token.split(".")[1]
                # Pad for base64 decoding
                payload += "=" * ((4 - len(payload) % 4) % 4)
                decoded = base64.b64decode(payload)
                claims = json.loads(decoded)
                return claims.get("user_id", claims.get("sub", "local_user"))
            except Exception as e:
                pass # Fallback to hashing
        
        # If it's still too long, hash it
        if len(token) > 50:
            import hashlib
            return hashlib.md5(token.encode()).hexdigest()
            
        return token


    # Firebase Authentication Mode
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required.")
        
    token = credentials.credentials
    try:
        import firebase_admin
        from firebase_admin import auth, credentials as firebase_credentials
        
        if not firebase_admin._apps:
            # Check if GOOGLE_APPLICATION_CREDENTIALS or FIREBASE_SERVICE_ACCOUNT is set
            service_account_json = os.getenv("FIREBASE_SERVICE_ACCOUNT")
            if service_account_json:
                cred_dict = json.loads(service_account_json)
                cred = firebase_credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
            else:
                # Fallback to default credentials (e.g. GOOGLE_APPLICATION_CREDENTIALS)
                firebase_admin.initialize_app()
                
        decoded_token = auth.verify_id_token(token)
        return decoded_token["uid"]
    except Exception as e:
        logger.error(f"Auth error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token.")

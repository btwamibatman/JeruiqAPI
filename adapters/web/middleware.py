from flask import request, abort
from adapters.auth.jwt_auth import JWTAuthService

jwt_service = JWTAuthService()

def require_jwt():
    token = request.headers.get("Authorization")
    if not token:
        abort(401, description="Unauthorized")
    try:
        jwt_service.verify_token(token)
    except ValueError as e:
        abort(401, description=str(e))
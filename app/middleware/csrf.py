from fastapi import Request, HTTPException, status
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import secrets
from typing import Optional, Tuple
import time

class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        csrf_token_key: str = "_csrf_token",
        max_token_age: int = 3600  # 1 hour
    ):
        super().__init__(app)
        self.csrf_token_key = csrf_token_key
        self.max_token_age = max_token_age
        self.safe_methods = {"GET", "HEAD", "OPTIONS"}

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method in self.safe_methods:
            # Generate new token for GET requests
            token, timestamp = self._generate_csrf_token()
            request.state.csrf_token = token
            response = await call_next(request)
            # Store token and timestamp in session
            request.state.session.set(self.csrf_token_key, {
                "token": token,
                "timestamp": timestamp
            })
            return response
        
        # For unsafe methods, verify CSRF token
        session_data = request.state.session.get(self.csrf_token_key, {})
        session_token = session_data.get("token")
        token_timestamp = session_data.get("timestamp", 0)
        
        request_token = (
            request.headers.get("X-CSRF-TOKEN") or
            request.form().get(self.csrf_token_key)
        )

        if not self._is_valid_token(session_token, request_token, token_timestamp):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="CSRF token verification failed"
            )

        # Generate new token after successful validation
        new_token, new_timestamp = self._generate_csrf_token()
        request.state.csrf_token = new_token
        response = await call_next(request)
        
        # Store new token in session
        request.state.session.set(self.csrf_token_key, {
            "token": new_token,
            "timestamp": new_timestamp
        })
        
        return response

    def _generate_csrf_token(self) -> Tuple[str, int]:
        """Generate a new CSRF token with timestamp"""
        return secrets.token_urlsafe(32), int(time.time())

    def _is_valid_token(
        self,
        session_token: Optional[str],
        request_token: Optional[str],
        timestamp: int
    ) -> bool:
        """Validate token and check if it's expired"""
        if not session_token or not request_token:
            return False
            
        # Check if token is expired
        current_time = int(time.time())
        if current_time - timestamp > self.max_token_age:
            return False
            
        # Compare tokens in constant time
        return secrets.compare_digest(session_token, request_token)

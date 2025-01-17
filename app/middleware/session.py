from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from itsdangerous import URLSafeSerializer
from typing import Optional
import json
import os
from dotenv import load_dotenv

load_dotenv()

class SessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, secret_key: Optional[str] = None):
        super().__init__(app)
        self.secret_key = secret_key or os.getenv("SECRET_KEY", "your-secret-key")
        self.serializer = URLSafeSerializer(self.secret_key)
        self.cookie_name = "session"
        self.max_age = 14 * 24 * 60 * 60  # 14 days

    async def dispatch(self, request: Request, call_next):
        session_data = self.load_session(request)
        request.state.session = Session(session_data)
        
        response = await call_next(request)
        
        if hasattr(request.state, "session"):
            self.save_session(request.state.session, response)
        
        return response

    def load_session(self, request: Request) -> dict:
        session_cookie = request.cookies.get(self.cookie_name)
        if not session_cookie:
            return {}
        
        try:
            return self.serializer.loads(session_cookie)
        except:
            return {}

    def save_session(self, session, response: Response):
        if not session.modified:
            return

        session_data = session.data
        session_cookie = self.serializer.dumps(session_data)
        
        response.set_cookie(
            key=self.cookie_name,
            value=session_cookie,
            max_age=self.max_age,
            httponly=True,
            samesite="lax"
        )


class Session:
    def __init__(self, initial_data: dict = None):
        self.data = initial_data or {}
        self.modified = False
        self._flash = self.data.pop("_flash", {})
        self._flash_new = {}

    def get(self, key: str, default=None):
        """Get a session value"""
        return self.data.get(key, default)

    def set(self, key: str, value):
        """Set a session value"""
        self.data[key] = value
        self.modified = True

    def pop(self, key: str, default=None):
        """Remove and return a session value"""
        self.modified = True
        return self.data.pop(key, default)

    def clear(self):
        """Clear all session data"""
        self.data.clear()
        self.modified = True

    def flash(self, key: str, value):
        """Set a flash message"""
        self._flash_new[key] = value
        self.modified = True

    def get_flash(self, key: str, default=None):
        """Get a flash message"""
        return self._flash.get(key, default)

    def has(self, key: str) -> bool:
        """Check if key exists in session"""
        return key in self.data

from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse
from typing import Optional
from functools import wraps

def login_required(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        if not request.state.session.get("user_id"):
            return RedirectResponse(url="/login", status_code=302)
        return await func(request, *args, **kwargs)
    return wrapper

def get_current_user_id(request: Request) -> Optional[int]:
    """Get the current user ID from session"""
    return request.state.session.get("user_id")

def is_authenticated(request: Request) -> bool:
    """Check if the user is authenticated"""
    return bool(request.state.session.get("user_id"))

from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response
from starlette.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, auth
from fastapi.templating import Jinja2Templates
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

def get_current_user_or_none(token: str = None, db: Session = Depends(get_db)):
    """Get current user without raising an exception"""
    if not token:
        return None
    try:
        return auth.get_current_user(token, db)
    except HTTPException:
        return None

@router.get("/")
async def home(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user)
):
    return templates.TemplateResponse(
        "pages/home.html",
        {
            "request": request,
            "user": current_user
        }
    )

@router.get("/users")
async def list_users(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        "pages/users/index.html",
        {"request": request, "users": users, "user": current_user}
    )

@router.get("/properties")
async def list_properties(
    request: Request,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    properties = db.query(models.Site).all()
    return templates.TemplateResponse(
        "pages/properties/index.html",
        {
            "request": request,
            "properties": properties,
            "user": current_user
        }
    )

@router.get("/login")
async def login_page(
    request: Request,
    current_user: models.User = Depends(get_current_user_or_none)
):
    if current_user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "error": None
        }
    )

@router.post("/login")
async def login(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Login attempt for email: {email}")
        user = auth.authenticate_user(db, email, password)
        
        if not user:
            logger.warning(f"Failed login attempt for email: {email}")
            return templates.TemplateResponse(
                "auth/login.html",
                {
                    "request": request,
                    "error": "Invalid email or password",
                    "email": email
                },
                status_code=400
            )
        
        # Create JWT token
        access_token = auth.login_user(user)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24  # 24 hours
        )
        
        logger.info(f"Successful login for user: {user.email}")
        return response
        
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return templates.TemplateResponse(
            "auth/login.html",
            {
                "request": request,
                "error": "An error occurred. Please try again.",
                "email": email
            },
            status_code=500
        )

@router.get("/register")
async def register_page(
    request: Request,
    current_user: models.User = Depends(get_current_user_or_none)
):
    if current_user:
        return RedirectResponse(url="/", status_code=302)
    return templates.TemplateResponse(
        "auth/register.html",
        {
            "request": request,
            "error": None
        }
    )

@router.post("/register")
async def register(
    request: Request,
    response: Response,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        logger.info(f"Registration attempt for email: {email}")
        
        # Check if user already exists
        db_user = auth.get_user(db, email=email)
        if db_user:
            logger.warning(f"Registration failed - email already exists: {email}")
            return templates.TemplateResponse(
                "auth/register.html",
                {
                    "request": request,
                    "error": "Email already registered",
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                },
                status_code=400
            )
        
        # Create user
        user_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        
        user = auth.create_user(db, user_data)
        logger.info(f"Successfully registered user: {user.email}")
        
        # Create JWT token
        access_token = auth.login_user(user)
        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24  # 24 hours
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return templates.TemplateResponse(
            "auth/register.html",
            {
                "request": request,
                "error": "An error occurred. Please try again.",
                "first_name": first_name,
                "last_name": last_name,
                "email": email
            },
            status_code=500
        )

@router.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(key="token")
    return response

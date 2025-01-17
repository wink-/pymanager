from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from . import models
from .database import engine
from .routes import api, web

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Property Manager",
    description="Property management system built with FastAPI",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(web.router, tags=["web"])
app.include_router(api.router, prefix="/api", tags=["api"])

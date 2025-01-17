from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth
from typing import List

router = APIRouter(prefix="/api")

@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, email, password)
    if not user:
        request.state.session.flash("error", "Invalid email or password")
        return RedirectResponse(url="/login", status_code=302)
    
    auth.login_user(request, user)
    return RedirectResponse(url="/", status_code=302)

@router.post("/users")
async def create_user(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = auth.get_user(db, email=email)
    if db_user:
        request.state.session.flash("error", "Email already registered")
        return RedirectResponse(url="/register", status_code=302)
    
    user_data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name
    }
    
    user = auth.create_user(db, user_data)
    auth.login_user(request, user)
    return RedirectResponse(url="/", status_code=302)

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "success"}

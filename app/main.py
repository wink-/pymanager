from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, auth
from .database import engine, get_db
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = auth.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(
        email=user.email,
        hashed_password=auth.get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/sites/", response_model=schemas.Site)
def create_site(site: schemas.SiteCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_site = models.Site(**site.dict(), owner_id=current_user.id)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

@app.get("/sites/", response_model=List[schemas.Site])
def read_sites(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    sites = db.query(models.Site).filter(models.Site.owner_id == current_user.id).offset(skip).limit(limit).all()
    return sites

@app.post("/sites/{site_id}/structures/", response_model=schemas.Structure)
def create_structure(site_id: int, structure: schemas.StructureCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    site = db.query(models.Site).filter(models.Site.id == site_id, models.Site.owner_id == current_user.id).first()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    db_structure = models.Structure(**structure.dict(), site_id=site_id)
    db.add(db_structure)
    db.commit()
    db.refresh(db_structure)
    return db_structure

@app.post("/structures/{structure_id}/rooms/", response_model=schemas.Room)
def create_room(structure_id: int, room: schemas.RoomCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    structure = db.query(models.Structure).join(models.Site).filter(
        models.Structure.id == structure_id,
        models.Site.owner_id == current_user.id
    ).first()
    if not structure:
        raise HTTPException(status_code=404, detail="Structure not found")
    db_room = models.Room(**room.dict(), structure_id=structure_id)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/structures/{structure_id}/rooms/", response_model=List[schemas.Room])
def read_rooms(structure_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    rooms = db.query(models.Room).join(models.Structure).join(models.Site).filter(
        models.Structure.id == structure_id,
        models.Site.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return rooms

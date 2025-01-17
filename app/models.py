from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sites = relationship("Site", back_populates="owner")

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="sites")
    structures = relationship("Structure", back_populates="site")

class Structure(Base):
    __tablename__ = "structures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"))
    
    site = relationship("Site", back_populates="structures")
    rooms = relationship("Room", back_populates="structure")

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    structure_id = Column(Integer, ForeignKey("structures.id"))
    length = Column(Float)
    width = Column(Float)
    height = Column(Float)
    wall_color = Column(String)
    floor_type = Column(String)
    notes = Column(Text)
    
    structure = relationship("Structure", back_populates="rooms")

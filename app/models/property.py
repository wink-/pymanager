from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Owner(BaseModel):
    __tablename__ = "owners"

    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255))
    phone_number = Column(String(20))
    created_by_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    created_by = relationship("User", back_populates="created_owners")
    sites = relationship("Site", back_populates="owner")

class Site(BaseModel):
    __tablename__ = "sites"

    name = Column(String(255))
    street_address = Column(String(255))
    city = Column(String(100))
    state = Column(String(50))
    zip_code = Column(String(20))
    
    owner_id = Column(Integer, ForeignKey('owners.id'))
    created_by_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    owner = relationship("Owner", back_populates="sites")
    created_by = relationship("User", back_populates="created_sites")
    structures = relationship("Structure", back_populates="site")

class Structure(BaseModel):
    __tablename__ = "structures"

    name = Column(String(100))  # e.g., Main House, Garage, Barn
    site_id = Column(Integer, ForeignKey('sites.id'))
    
    # Structure details
    num_floors = Column(Integer)
    num_entrances = Column(Integer)
    foundation_type = Column(String(100))
    total_square_footage = Column(Float)
    
    # Store square footage per floor as JSON string
    # e.g., {"1": 1000, "2": 800, "basement": 1000}
    floor_square_footage = Column(Text)  
    
    # Exterior details
    exterior_wall_material = Column(String(100))
    exterior_wall_color = Column(String(100))
    
    # Relationships
    site = relationship("Site", back_populates="structures")
    rooms = relationship("Room", back_populates="structure")
    maintenance_items = relationship("MaintenanceItem", back_populates="structure")

class Room(BaseModel):
    __tablename__ = "rooms"

    name = Column(String(100))
    structure_id = Column(Integer, ForeignKey('structures.id'))
    floor_number = Column(Integer)
    
    # Measurements
    perimeter = Column(Float)
    area = Column(Float)
    ceiling_height = Column(Float)
    peak_height = Column(Float)
    
    # Features
    num_outlets = Column(Integer)
    floor_type = Column(String(100))
    wall_paint_color = Column(String(100))
    trim_paint_color = Column(String(100))
    ceiling_paint_color = Column(String(100))
    
    # Relationships
    structure = relationship("Structure", back_populates="rooms")
    appliances = relationship("Appliance", back_populates="room")
    maintenance_items = relationship("MaintenanceItem", back_populates="room")

from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel

class Contractor(BaseModel):
    __tablename__ = "contractors"

    company_name = Column(String(255))
    contact_name = Column(String(255))
    phone = Column(String(20))
    email = Column(String(255))
    website = Column(String(255))
    notes = Column(Text)
    
    # Relationships
    maintenance_items = relationship("MaintenanceItem", back_populates="contractor")

class MaintenanceItem(BaseModel):
    __tablename__ = "maintenance_items"

    title = Column(String(255))
    description = Column(Text)
    cost = Column(Float)
    
    # Dates
    performed_date = Column(DateTime)
    next_maintenance_date = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_interval_days = Column(Integer, nullable=True)
    
    # Paint specific fields (nullable if not paint)
    paint_brand = Column(String(100), nullable=True)
    paint_color_number = Column(String(100), nullable=True)
    
    # Foreign keys
    contractor_id = Column(Integer, ForeignKey('contractors.id'), nullable=True)
    structure_id = Column(Integer, ForeignKey('structures.id'), nullable=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=True)
    appliance_id = Column(Integer, ForeignKey('appliances.id'), nullable=True)
    
    # Relationships
    contractor = relationship("Contractor", back_populates="maintenance_items")
    structure = relationship("Structure", back_populates="maintenance_items")
    room = relationship("Room", back_populates="maintenance_items")
    appliance = relationship("Appliance", back_populates="maintenance_items")

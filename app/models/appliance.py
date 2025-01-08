from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Appliance(BaseModel):
    __tablename__ = "appliances"

    name = Column(String(255))
    model_number = Column(String(100))
    serial_number = Column(String(100))
    manufacturer = Column(String(255))
    
    # Purchase information
    purchase_date = Column(DateTime)
    purchase_price = Column(Float)
    purchase_source = Column(String(255))
    
    # Warranty information
    warranty_start_date = Column(DateTime)
    warranty_end_date = Column(DateTime)
    warranty_details = Column(Text)
    
    # Location
    room_id = Column(Integer, ForeignKey('rooms.id'))
    
    # Notes
    maintenance_notes = Column(Text)
    general_notes = Column(Text)
    
    # Relationships
    room = relationship("Room", back_populates="appliances")
    maintenance_items = relationship("MaintenanceItem", back_populates="appliance")

from pydantic import BaseModel
from typing import List, Optional

class RoomBase(BaseModel):
    name: str
    length: float
    width: float
    height: float
    wall_color: str
    floor_type: str
    notes: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    structure_id: int

    class Config:
        from_attributes = True

class StructureBase(BaseModel):
    name: str

class StructureCreate(StructureBase):
    pass

class Structure(StructureBase):
    id: int
    site_id: int
    rooms: List[Room] = []

    class Config:
        from_attributes = True

class SiteBase(BaseModel):
    name: str
    address: str

class SiteCreate(SiteBase):
    pass

class Site(SiteBase):
    id: int
    owner_id: int
    structures: List[Structure] = []

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    sites: List[Site] = []

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

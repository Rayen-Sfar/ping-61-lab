from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TPBase(BaseModel):
    title: str
    description: str
    instructions: str
    difficulty: str = "Moyen"
    duration: str = "2h"
    vm_type: str
    status: str = "Published"


class TPCreate(TPBase):
    created_by: str


class TPUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    difficulty: Optional[str] = None
    duration: Optional[str] = None
    vm_type: Optional[str] = None
    status: Optional[str] = None


class TP(TPBase):
    id: int
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TPList(BaseModel):
    id: int
    title: str
    description: str
    difficulty: str
    duration: str
    vm_type: str
    created_by: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

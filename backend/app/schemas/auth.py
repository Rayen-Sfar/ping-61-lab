from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str
    role: str


class UserSchema(BaseModel):
    id: int
    cas_id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr

class UserDB(BaseModel) :
    username: str = Field(..., title="Username", min_length=3, max_length=20)
    password: str = Field(...,title="Password",min_length=8,max_length=12)
    email: EmailStr = Field(...,title="Email")
    profile_image: Optional[str] = Field(default=None,title="Profile Image")  
    about: Optional[str] = Field(default=None,title="About",min_length=20,max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), title="Created At")

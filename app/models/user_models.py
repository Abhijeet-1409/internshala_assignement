from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, EmailStr

class UserDB(BaseModel) :
    username: str = Field(title="Username", min_length=3, max_length=20)
    password: str = Field(title="Password",min_length=20)
    email: EmailStr = Field(title="Email")
    about: str = Field(title="About",min_length=20,max_length=300)
    profile_image: Optional[str] = Field(default=None,title="Profile Image")  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), title="Created At")

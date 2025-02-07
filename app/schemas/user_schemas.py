import pytz
from bson import ObjectId
from typing import Optional 
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from app.utils.field_validation_utils import objectid_to_str


class UserResponse(BaseModel):
    username: str = Field(title="Username", min_length=3, max_length=20)
    email: EmailStr = Field(title="Email")
    profile_image: HttpUrl = Field(title="Profile Image")  
    about: str = Field(title="About",min_length=20,max_length=300)
    created_at: datetime = Field(title="Created At")

    class Config:
        arbitrary_types_allowed = True
        extra = "ignore" 
        json_encoders = {
            datetime: lambda v: v.astimezone(pytz.utc).isoformat() if v else None  # Ensure UTC format for serialization
        }
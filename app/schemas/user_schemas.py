import pytz
from bson import ObjectId
from typing import Optional 
from datetime import datetime
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from app.utils.field_validation_utils import objectid_to_str


class UserResponse(BaseModel):
    id: ObjectId = Field(...,title="User Id")
    username: str = Field(..., title="Username", min_length=3, max_length=20)
    email: EmailStr = Field(...,title="Email")
    profile_image: Optional[HttpUrl] = Field(default=None,title="Profile Image")  
    about: Optional[str] = Field(default=None,title="About",min_length=20,max_length=100)
    created_at: datetime = Field(...,title="Created At")

    class Config:
        orm_mode = True  
        extra = "ignore" 
        json_encoders = {
            ObjectId: objectid_to_str,  
            datetime: lambda v: v.astimezone(pytz.utc).isoformat() if v else None  # Ensure UTC format for serialization
        }

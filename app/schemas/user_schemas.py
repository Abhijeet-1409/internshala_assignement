from typing import Optional 
from pydantic import BaseModel, EmailStr, HttpUrl, Field


class UserResponse(BaseModel):
    id: str = Field(...,title="User Id")
    username: str = Field(..., title="Username", min_length=3, max_length=20)
    email: EmailStr = Field(...,title="Email")
    profile_image: Optional[HttpUrl] = Field(default=None,title="Profile Image")  
    about: Optional[str] = Field(default=None,title="About",min_length=20,max_length=100)

    model_config={"extra":"ignore"}

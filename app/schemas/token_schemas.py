from bson import ObjectId
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.utils.field_validation_utils import objectid_to_str


class Token(BaseModel):
    access_token: str = Field(title="Access token")
    token_type: str = Field(title="Bearer")


class TokenData(BaseModel):
    exp: Optional[datetime] = Field(default=None,title="Exp")
    username: Optional[str] = Field(default=None,title="Username")
    user_id: Optional[ObjectId] = Field(default=None,title="User id")


    class Config :
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: objectid_to_str,  # Convert ObjectId to string
        }
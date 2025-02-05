from bson import ObjectId
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(...,title="Access token")
    token_type: str = Field(...,title="Bearer")
    expire_time: str = Field(...,title="Expire time")


class TokenData(BaseModel):
    exp: Optional[datetime] = Field(default=None,title="Exp")
    username: Optional[str] = Field(default=None,title="Username")
    user_id: Optional[ObjectId] = Field(default=None,title="User id")


    class Config :
        arbitrary_types_allowed = True
from typing import Optional 
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utils.field_validation_utils import check_username_validity, check_password_validity,check_email_validity

class UserCreate(BaseModel) :
    username: str = Field(title="Username", min_length=3, max_length=20)
    password: str = Field(title="Password",min_length=8,max_length=12)
    email: EmailStr = Field(title="Email")
    about: str = Field(title="About",min_length=20,max_length=300)
    

    @field_validator('username') 
    def validate_username(cls,value) :
        return check_username_validity(value)

    @field_validator('password')
    def validate_password(cls,value) :
        return check_password_validity(value)
    
    @field_validator('email')
    def validate_email(cls,value):
        return check_email_validity(value)
    
    class Config:
        extra="ignore"


class UserLogin(BaseModel) :
    username: str = Field(..., title="Username", min_length=3, max_length=20)
    password: str = Field(...,title="Password",min_length=8,max_length=12)

    @field_validator('username') 
    def validate_username(cls,value) :
        return check_username_validity(value)

    @field_validator('password')
    def validate_password(cls,value) :
        return check_password_validity(value)
    




    
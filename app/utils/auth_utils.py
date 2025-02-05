import jwt
from typing import Optional
from jwt import InvalidTokenError
from typing import Annotated, Any
from app.config.config import settings
from passlib.context import CryptContext
from app.schemas.token_schemas import TokenData
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str :
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,settings.secret_key,algorithm=settings.algorithm)
    
    return encoded_jwt


async def get_token_data(token: Annotated[str,Depends(oauth2_scheme)]) -> TokenData :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try :
        payload: dict = jwt.decode(token,settings.secret_key,algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        exp: datetime = payload.get('exp')

        if user_id is None or username is None:
            raise credentials_exception
    
    except InvalidTokenError :
        raise credentials_exception
    
    return TokenData(username=username,user_id=user_id,exp=exp)

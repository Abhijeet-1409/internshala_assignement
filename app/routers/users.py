from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_schemas import UserResponse
from app.services.auth_services import AuthenticationService
from app.utils.auth_utils import get_token_data
from app.schemas.token_schemas import TokenData

router = APIRouter(tags=["Users"])


@router.get("/profile", response_model=UserResponse)
async def get_profile(
    token_data: Annotated[TokenData, Depends(get_token_data)], #Use the token to get user data
    auth_service: AuthenticationService = Depends(AuthenticationService)
    ):
    
    try:

        user: UserResponse | None = await auth_service.get_current_user(token_data) #Get the user from token

        if user is None :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated. Please provide valid credentials.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return user 

    except HTTPException as http_exc:
        raise http_exc
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error",
        )

from bson import ObjectId
from datetime import timedelta
from app.db.database import Database
from app.config.config import settings
from typing import Annotated, Optional
from app.errors.errors import CustomFileError
from app.logger.custom_logger import custom_logger
from fastapi.responses import JSONResponse
from app.schemas.token_schemas import Token
from pydantic import EmailStr,  ValidationError
from app.utils.auth_utils import ValidatedFile, create_access_token
from app.schemas.auth_schemas import UserCreate,UserLogin
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status , BackgroundTasks
from app.services.auth_services import AuthenticationService, UserCreationInconsistencyError, ProfileUpdateInconsistencyError

router = APIRouter(tags=["Authenticaiton"])


@router.post("/login", response_model=Token)
async def login(
    user_login: Annotated[UserLogin,Form()], 
    auth_service: AuthenticationService = Depends(AuthenticationService),
    ):
    
    username: str = user_login.username
    password: str = user_login.password

    user_id: Optional[str] = await auth_service.check_credentials(username=username,password=password)

    if  user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token: str = create_access_token(
        data={"sub": username,"user_id":user_id}, 
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token,token_type="bearer")



@router.post("/register")
async def register(
        background_task: BackgroundTasks,
        username: str = Form(
            min_length=3,
            max_length=20,
            description="Username must start with an underscore (`_`) or an alphabet (A-Z, a-z). "
                        "It should contain at least one number and at least one special character. "
                        "Allowed special characters are: `_`, `@`, and `$`."
        ),
        password: str = Form(
            min_length=8,
            max_length=12,
            description="Password must start with an alphabet (A-Z, a-z). "
                        "It should contain at least one number and at least one special character. "
                        "Allowed special characters are: `$`, `@`, and `$`."
        ),
        email: EmailStr = Form(
            description="User's email address. Must be a valid email format."
        ),
        about: str = Form(
            min_length=20,
            max_length=300,
            description="A brief description about the user. Must be between 20 and 300 characters long."
        ),
        file: UploadFile = File(
            description="An image file for the user. Accepted formats are .png , .jpg or .jpeg.", 
        ),
        auth_service: AuthenticationService = Depends(AuthenticationService),
    ):

    try:
        
        valid_file: ValidatedFile = await auth_service.check_file_valid(file)

        # User Validation
        user:UserCreate = UserCreate(username=username,password=password,about=about,email=email)

        user_id: ObjectId = await auth_service.create_user(user=user,file=valid_file)
            
        return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "user_id": str(user_id),
                    "message": "User created successfully."
                }
            )    
    
    except HTTPException as http_exe:
        raise http_exe
    
    except CustomFileError as cusfilex:

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "File validation failed", "message": str(cusfilex)}
        )

    except ValidationError as valexe :
       
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
             detail=[{"loc": err["loc"], "msg": err["msg"]} for err in valexe.errors()]
        )

    except Exception as exe:
        custom_logger.exception(f"Unexpected error: {exe}")


        if isinstance(exe,UserCreationInconsistencyError) :   
            rollback_id:ObjectId = exe.user_id
            background_task.add_task(auth_service.rollback_user,user_id=rollback_id)
        
        elif isinstance(exe,ProfileUpdateInconsistencyError) :
            rollback_id:ObjectId = exe.user_id
            rollback_object_key:str = exe.profile_image_url
            background_task.add_task(auth_service.rollback_user,user_id=rollback_id)
            background_task.add_task(auth_service.rollback_image,object_key=rollback_object_key)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )
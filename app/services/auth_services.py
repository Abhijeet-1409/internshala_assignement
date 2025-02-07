import aioboto3
from bson import ObjectId
from typing import  Literal
from app.config.config import settings
from app.db.database import Database
from app.models.user_models import UserDB
from app.schemas.auth_schemas import UserCreate
from app.schemas.user_schemas import UserResponse
from app.schemas.token_schemas import TokenData
from app.logger.custom_logger import custom_logger
from app.utils.auth_utils import ValidatedFile, get_password_hash, verify_password
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import  HTTPException, UploadFile , status
from pymongo.results import InsertOneResult,DeleteResult,UpdateResult
from app.errors.errors import CustomFileError, UserCreationInconsistencyError, ProfileUpdateInconsistencyError
from app.utils.field_validation_utils import objectid_to_str 

S3_Operations = Literal["get_object", "put_object", "delete_object"]


class AuthenticationService: 

    def __init__(self):  
        self.db: Database = Database()
        

    async def create_user(self,user: UserCreate,file: ValidatedFile) -> ObjectId :
        """Create a new user in the database."""
        
        try :
            
            is_exist = await self.check_user_exits(username = user.username, email = user.email) 
            
            if is_exist:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"messasge": "User already exists with username or email"}
                )
            
            user_data: dict = user.model_dump()
            print(user_data)
            user_data['password'] = get_password_hash(password = user_data['password'])
            user_db = UserDB(**user_data)
            user_db_bson = user_db.model_dump()
            result_obj: InsertOneResult = await self.db.user_collection.insert_one(user_db_bson)
            user_id = result_obj.inserted_id

            if user_id is None :
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error."
                )
        
            profile_image_url: str = await self.upload_image(
                user_id = user_id,
                username = user.username,
                profile_image = file
            )
            
            update_obj: UpdateResult = await self.db.user_collection.update_one(
                {"_id": user_id},
                {"$set": {"profile_image": profile_image_url}}
            )

            if update_obj.modified_count == 0 :
                raise ProfileUpdateInconsistencyError(
                    user_id=user_id,
                    profile_image_url=profile_image_url
                )

            return user_id

        except HTTPException as http_exe :
            raise http_exe      
        except Exception as exe :
            custom_logger.exception(f"Unexpected error: {exe}")
            raise exe
        


    async def get_current_user(self,token_data:TokenData) -> UserResponse | None :
        """Retrieve the currently authenticated user based on the provided token."""
        
        try : 
            
            user_id = token_data.user_id
            user_doc = await self.db.user_collection.find_one({"_id":user_id})

            if not user_doc:
                return None

            user_data: dict = dict(user_doc)
            object_key = user_data.get('profile_image')

            if object_key:  
                user_data["profile_image"] = await self.generate_presigned_url(
                    object_key=object_key, operation="get_object"
                )
            
            return  UserResponse(**user_data)
        
        except Exception as exe :
            custom_logger.exception(f"Unexpected error: {exe}")
            raise exe



    async def rollback_user(self ,user_id: ObjectId) -> None:
        """Background task for deletion of user."""
        
        try:
            user_doc: DeleteResult = await self.db.user_collection.delete_one({"_id": user_id})

            if user_doc.deleted_count == 0:
                custom_logger.info(f"User with id '{objectid_to_str(user_id)}' not found. Deletion failed.")
            else:
                custom_logger.info(f"User with id '{objectid_to_str(user_id)}' successfully deleted.")
    
        except Exception as exe:
            custom_logger.error(f"An error occurred while trying to delete user '{objectid_to_str(user_id)}': {exe}")

    

    async def rollback_image(self , object_key: str) -> None:
        """Background task for deletion of user profile image."""
    
        region_name = settings.aws_bucket_region
        aws_access_key = settings.aws_access_key
        aws_secret_key = settings.aws_secret_key
        bucket_name = settings.bucket_name
        
        session = aioboto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

        async with session.client("s3") as s3_client:
            try:
                await s3_client.delete_object(Bucket=bucket_name, Key=object_key)
            except (BotoCoreError, ClientError) as botoexe:
                custom_logger.error(f"BotoCoreError/ClientError occurred: {botoexe}")
            except Exception as exe :
                custom_logger.exception(f"Unexpected error: {exe}")
            
    

    async def upload_image(self,user_id: ObjectId, username: str, profile_image: ValidatedFile) -> str:
        """Upload a profile image for the given user."""
        
        region_name = settings.aws_bucket_region
        aws_access_key = settings.aws_access_key
        aws_secret_key = settings.aws_secret_key
        bucket_name = settings.bucket_name
        bucket_folder_name = settings.bucket_folder_name


        key = f"{bucket_folder_name}/{username}/{profile_image.filename}"

        session = aioboto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )   

        async with session.client("s3") as s3_client:
            try:
                
                response = await s3_client.put_object(
                    Bucket=bucket_name,
                    Key=key,
                    Body=profile_image.content,
                    ContentType=profile_image.content_type
                )
                custom_logger.info(f"Image uploaded successfully")
                return key
            
            except (BotoCoreError, ClientError) as botoexe:
                custom_logger.error(f"BotoCoreError/ClientError occurred: {botoexe}")
                raise UserCreationInconsistencyError(user_id=user_id)
            except Exception as exe :
                custom_logger.exception(f"Unexpected error: {exe}")
                raise UserCreationInconsistencyError(user_id=user_id)



    async def generate_presigned_url(self, object_key : str,operation: S3_Operations) -> str:
        """Generate a pre-signed URL for files securely."""

        region_name = settings.aws_bucket_region
        aws_access_key = settings.aws_access_key
        aws_secret_key = settings.aws_secret_key
        expiration = settings.aws_expiration
        bucket_name = settings.bucket_name
        
        match operation :
            case "get_object" | "put_object" | "delete_object":
                params = {"Bucket": bucket_name, "Key": object_key}
            case _ :
                raise ValueError("Invalid operation.  Must be 'get_object' , 'put_object' or 'delete_obj'.") #handle invalid operations
        
        session = aioboto3.Session( 
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

        async with session.client("s3") as s3_client:
            try:
                url = await s3_client.generate_presigned_url(
                    operation,
                    Params=params,
                    ExpiresIn=expiration
                )
                custom_logger.info(f"Presigned URL generated: ")
                return url
            
            except Exception as exe:
                custom_logger.exception(f"Unexpected error: {exe}")
                raise exe
    


    async def check_file_valid(self,file: UploadFile) -> ValidatedFile:
        MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
        ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

        try:
            filename = file.filename.lower()
            content_type = file.content_type

            if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                raise CustomFileError("Invalid file format. Allowed formats: .png, .jpg, .jpeg")

            file_content: bytes = await file.read()
            file_size = len(file_content)

            if file_size > MAX_FILE_SIZE:
                raise CustomFileError("File size must be less than 2MB.")

            return ValidatedFile(filename=filename, content=file_content,content_type=content_type)

        except Exception as ex:
            raise ex



    async def check_user_exits(self,username: str,email: str) -> bool:
        """Check if user exists with given username or email."""

        existing_doc = await self.db.user_collection.find_one({
            "$or":[ 
                {"username": username},
                {"email": email}
            ]
        })

        if existing_doc :
            return True

        return False
    


    async def check_credentials(self, username: str, password: str) -> str | None:
        """Check if the provided credentials are valid."""
        
        user: dict | None = await self.db.user_collection.find_one({"username": username})

        if user is None :
            return None
        
        hashed_password: str = user['password']

        if not verify_password(plain_password=password,hashed_password=hashed_password) :
            return None
        
        return objectid_to_str(user["_id"])
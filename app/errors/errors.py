from bson import ObjectId


class CustomFileError(Exception):
    """Custom exception for file-related errors."""
    
    def __init__(self, message: str):
        super().__init__(message)  



class UserCreationInconsistencyError(Exception):
    """Raised when the user document is inserted but the profile image upload fails."""

    def __init__(self, user_id: ObjectId, message="User created, but profile image upload failed."):
        super().__init__(message)
        self.user_id: ObjectId = user_id


class ProfileUpdateInconsistencyError(Exception):
    """Raised when the profile image is uploaded but the database is not updated."""

    def __init__(self, user_id: ObjectId, profile_image_url: str, message="Profile image uploaded, but database update failed."):
        super().__init__(message)
        self.user_id: ObjectId = user_id
        self.profile_image_url: str = profile_image_url

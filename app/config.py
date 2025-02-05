import os
from pydantic_settings import BaseSettings , SettingsConfigDict

# Get the current file's directory
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

# Go up one level
parent_directory = os.path.dirname(current_directory)

# Construct the path to the .env file
env_file_path = os.path.join(parent_directory, '.env')


class Config(BaseSettings) :

    secret_key: str 
    mongodb_uri: str
    aws_access_key: str
    aws_secret_key: str
    bucket_name: str
    bucket_folder_name: str

    model_config = SettingsConfigDict(env_file=env_file_path)

settings = Config()

if __name__ == "__main__" :
    print(settings.model_dump())
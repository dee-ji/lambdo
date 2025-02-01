# from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings().model_dump()
try:
    api_token = settings["api_key"]
except KeyError:
    print("WARNING: You must have a valid Lambda Labs API Key")
    print("         Login to your account and go to API keys -> Generate API Key")
    print("         Add this key to a local .env file and assign it to 'API_KEY' to continue...")
    exit()
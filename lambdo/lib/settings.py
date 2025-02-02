# from pydantic import ValidationError
import os
import typer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '.env'),
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings().model_dump()
try:
    api_token = settings["api_key"]
    ssh_path = settings["ssh_path"]
    if '~/' in ssh_path:
        ssh_path = os.path.expanduser(ssh_path)
except KeyError:
    typer.echo("Uh oh, It looks like you haven't properly setup lambdo...")
    typer.echo(f"    Run `lambdo setup` to configure your local parameters")
    exit()
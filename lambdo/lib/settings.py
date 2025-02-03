import os
import typer
from pydantic_settings import BaseSettings, SettingsConfigDict


if not os.path.exists(os.path.join(os.path.dirname(__file__), '.env')):
    with open(os.path.join(os.path.dirname(__file__), ".env"), mode="w+") as f:
        f.write(f"API_KEY=put-your-api-key-here\n")
        f.write(f"SSH_PATH=put-your-ssh-path-here\n")


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
    if api_token == "put-your-api-key-here" or ssh_path == "put-your-ssh-path-here":
        api_key = typer.prompt("Enter your Lambda Labs API Key")
        ssh_path = typer.prompt("Enter your ssh key path")
        with open(os.path.join(os.path.dirname(__file__), ".env"), mode="w+") as f:
            f.write(f"API_KEY={api_key}\n")
            f.write(f"SSH_PATH={ssh_path}\n")
    if '~/' in ssh_path:
        ssh_path = os.path.expanduser(ssh_path)
except KeyError:
    typer.echo("Uh oh, It looks like you haven't properly setup lambdo...")
    typer.echo(f"    Run `lambdo setup` to configure your local parameters")
    exit()

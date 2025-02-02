import os
import typer
from typing_extensions import Annotated


app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    api_key: Annotated[str, typer.Option(prompt="Enter your Lambda Labs API Key")],
    ssh_path: Annotated[str, typer.Option(prompt="Enter your ssh key path")],
):
    """
    Setup command for lambdo that helps store your API Key and ssh path
    """
    if ctx.invoked_subcommand is not None:
        return
    # Create or overwrite the .env file that stores the API_KEY
    with open(os.path.join(os.path.dirname(__file__), "../lib/.env"), mode="w+") as f:
        f.write(f"API_KEY={api_key}\n")
        f.write(f"SSH_PATH={ssh_path}\n")
    typer.echo("Setup completed successfully!")

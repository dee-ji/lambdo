import os
import json
import typer
from typing_extensions import Annotated
from lambdo.lib.settings import ssh_path
from lambdo.lib.helpers import get_response, post_request, delete_request


app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Display SSH keys from the Lambda Labs Public Cloud API.

    By default, prints all SSH keys.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/ssh-keys | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/ssh-keys")

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("add", help="Add an SSH key")
def add_ssh_key(
    new: Annotated[bool, typer.Option("--new", "-n", help="Add a new SSH Key")] = False,
):
    # https://cloud.lambdalabs.com/api/v1/ssh-keys
    if new:
        key_name = typer.prompt("New SSH Key Name")
        data = {"name": key_name}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/ssh-keys", data=data
        )
        with open(os.path.join(ssh_path, f"{key_name}.pem"), "x") as f:
            f.write(resp.json()["data"]["private_key"])
        # Make sure to set the pem file to 400 "Read Only"
        os.chmod(os.path.join(ssh_path, f"{key_name}.pem"), 0o400)
        typer.echo(
            f"The new private key has been written to: {os.path.join(ssh_path, f"{key_name}.pem")}"
        )
    else:
        filename = typer.prompt("SSH Key filename")
        file = {"file": open(os.path.join(ssh_path, filename))}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/ssh-keys", files=file
        )

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("delete", help="Delete an SSH key")
def delete_ssh_key(
    key: Annotated[
        str,
        typer.Option(
            prompt="SSH Key ID",
            help="The id of the SSH key you want to delete",
        ),
    ],
):
    typer.echo(f"This action will permanently delete the key: {key}")
    delete = typer.confirm("Are you sure you want to delete this SSH key?")
    if not delete:
        raise typer.Abort()

    # https://cloud.lambdalabs.com/api/v1/ssh-keys/{id}
    resp = delete_request(url=f"https://cloud.lambdalabs.com/api/v1/ssh-keys/{key}")
    if resp.status_code == 200:
        typer.echo("SSH key was deleted successfully")
    else:
        typer.Exit(code=1)

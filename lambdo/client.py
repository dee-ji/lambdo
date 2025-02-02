import json
import os.path
from typing import Annotated

import typer
from lambdo.lib.helpers import get_response
from lambdo.sub_cmds import instance_types, ssh_keys


app = typer.Typer(
    help="Lambdo is a CLI tool that utilizes the Lambda GPU Cloud Public APIs"
)
app.add_typer(
    instance_types.app,
    name="instance-types",
    help="List the instances types offered by Lambda GPU Cloud",
)
app.add_typer(ssh_keys.app, name="ssh-keys", help="Manage SSH Keys for your instances")


def main():
    app()


@app.command(help="List your running instances")
def instances():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    print(json.dumps(resp.json(), indent=2))


@app.command(help="List your persistent storage filesystems")
def filesystems():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    print(json.dumps(resp.json(), indent=2))


@app.command(help="Setup the CLI with your API KEY")
def setup(
    api_key: Annotated[str, typer.Option(prompt="Enter your Lambda Labs API Key")],
    ssh_path: Annotated[str, typer.Option(prompt="Enter your ssh key path")],
):
    # Create or overwrite the .env file that stores the API_KEY
    with open(os.path.join(os.path.dirname(__file__), "lib/.env"), mode="w+") as f:
        f.write(f"API_KEY={api_key}\n")
        f.write(f"SSH_PATH={ssh_path}\n")
    typer.echo("Setup completed successfully!")


if __name__ == "__main__":
    main()

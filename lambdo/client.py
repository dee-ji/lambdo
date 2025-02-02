import json
import os.path
from typing import Annotated

import typer
from lambdo.lib.helpers import get_response
from lambdo.sub_cmds import instance_types


app = typer.Typer(help="Lambdo is a CLI built to utilize Lambda GPU Cloud Public APIs")
app.add_typer(instance_types.app, name="instance-types", help="List the instances types offered by Lambda GPU Cloud")


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
def setup(api_key: Annotated[str, typer.Option(prompt="Enter your Lambda Labs API Key")]):
    # Create or overwrite the .env file that stores the API_KEY
    with open(os.path.join(os.path.dirname(__file__), "lib/.env"), mode="w+") as f:
        f.write(f"API_KEY={api_key}")
    typer.echo("Setup completed successfully!")


if __name__ == "__main__":
    main()

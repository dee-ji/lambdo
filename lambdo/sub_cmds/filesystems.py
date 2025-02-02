import json
import typer
from lambdo.lib.helpers import get_response


app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Display SSH keys from the Lambda Labs Public Cloud API.

    By default, prints all SSH keys.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    typer.echo(json.dumps(resp.json(), indent=2))

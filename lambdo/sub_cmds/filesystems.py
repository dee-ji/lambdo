import json
import typer
from rich.table import Table
from rich.console import Console
from lambdo.lib.helpers import get_response


app = typer.Typer(
    invoke_without_command=True,
    add_completion=False
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False, "--debug", "-d", help="Print additional helpful information."
    ),
):
    """
    Display persistent storage filesystems from the Lambda Labs Public Cloud API.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems").json()[
        "data"
    ]
    if debug:
        typer.echo(json.dumps(resp, indent=2))
    # Create and add columns to filesystem table
    table = Table()
    table.add_column("ID", justify="right")
    table.add_column("Name", justify="right")
    table.add_column("Mount Point", justify="right")
    table.add_column("Created", justify="right")
    table.add_column("Created By", justify="right")
    table.add_column("In Use", justify="right")
    table.add_column("Region Name", justify="right")
    table.add_column("Description", justify="right")

    # Iterate over all filesystems and add each row to the table
    for fs in resp:
        this_id = fs["id"]
        name = fs["name"]
        mount_point = fs["mount_point"]
        created = fs["created"]
        created_by = fs["created_by"]["email"]
        in_use = "True" if fs["is_in_use"] else "False"
        region_name = fs["region"]["name"]
        region_desc = fs["region"]["description"]

        table.add_row(
            this_id,
            name,
            mount_point,
            created,
            created_by,
            in_use,
            region_name,
            region_desc,
        )

    # Create and print table
    console = Console()
    console.print(table)

import json
import typer
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated
from lambdo.lib.helpers import get_response


app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    available: bool = typer.Option(
        False, "--available", help="Show only available instance types."
    ),
    unavailable: bool = typer.Option(
        False, "--unavailable", help="Show only unavailable instance types."
    ),
):
    """
    Display instance types from the Lambda Labs Public Cloud API.

    By default, prints all instance types. Optionally, filter to only available or
    unavailable instance types using --available or --unavailable.
    """
    # If a subcommand (like gpu or location) is invoked, skip this callback.
    if ctx.invoked_subcommand is not None:
        return

    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(
        url="https://cloud.lambdalabs.com/api/v1/instance-types"
    ).json()["data"]

    # typer.echo(json.dumps(resp, indent=2))

    table = Table()
    table.add_column("GPU", justify="right")
    table.add_column("Locations", justify="right")
    table.add_column("Description", justify="right")
    table.add_column("Price Per Hour", justify="right")
    table.add_column("VCPUs", justify="right")
    table.add_column("Memory", justify="right")
    table.add_column("# of GPUs", justify="right")

    for gpu_data in resp:
        gpu_dict = resp[gpu_data]["instance_type"]

        # Get locations list
        available_locations = resp[gpu_data]["regions_with_capacity_available"]
        # Combine any locations found
        locations = (
            ",".join(n["name"] for n in available_locations)
            if len(available_locations) >= 1
            else None
        )
        # Assign all row items
        name = gpu_dict["name"]
        description = gpu_dict["description"]
        price = f'{gpu_dict["price_cents_per_hour"] / 100:.2f}'
        vcpus = str(gpu_dict["specs"]["vcpus"])
        vram = gpu_dict["specs"]["memory_gib"]
        vram = f"{vram}GB" if len(str(vram)) <= 3 else f"{vram / 1000:.2f}TB"
        num_gpus = str(gpu_dict["specs"]["gpus"])

        # Add table row based on available or unavailable
        if available and locations is None:
            continue
        elif unavailable and locations is not None:
            continue
        else:
            table.add_row(name, locations, description, price, vcpus, vram, num_gpus)
    # Print Table
    console = Console()
    console.print(table)


@app.command("gpu", help="Search for a particular GPU by name")
def get_gpu(
    name: Annotated[
        str, typer.Option("--name", "-n", help="Provide the name of the gpu")
    ],
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")
    typer.echo(json.dumps(resp.json()["data"][name], indent=2))


@app.command("location", help="Search for GPUs by location")
def get_location(
    name: Annotated[str, typer.Option("--name", "-n", help="Search by location")],
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")

    find_by_location = [
        loc
        for inst in resp.json()["data"]
        for loc in resp.json()["data"][inst]["regions_with_capacity_available"]
        if name.lower() in loc["description"].lower() or name.lower() in loc["name"]
    ]
    if find_by_location:
        available_instance = [
            resp.json()["data"][inst]
            for inst in resp.json()["data"]
            if find_by_location[0]
            in resp.json()["data"][inst]["regions_with_capacity_available"]
        ]
        typer.echo(json.dumps(available_instance, indent=2))
    else:
        typer.echo("There are currently no instances available...")

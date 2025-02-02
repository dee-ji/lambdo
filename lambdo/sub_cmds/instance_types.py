import json
import typer
from requests import Response
from typing_extensions import Annotated
from lambdo.lib.helpers import get_response


app = typer.Typer(invoke_without_command=True)


def filter_availability(
    data: Response, available: bool, unavailable: bool
) -> list | Response:
    """
    Filter the data list based on the available or unavailable flags.
    It is an error to provide both.
    """
    if available and unavailable:
        typer.echo("Error: Cannot set both --available and --unavailable.")
        raise typer.Exit(code=1)
    if available:
        return [
            inst
            for inst in data.json()["data"]
            if data.json()["data"][inst]["regions_with_capacity_available"]
        ]
    elif unavailable:
        return [
            inst
            for inst in data.json()["data"]
            if not data.json()["data"][inst]["regions_with_capacity_available"]
        ]
    else:
        return data


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
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")

    data = filter_availability(resp, available, unavailable)

    if available:
        print(json.dumps(data, indent=2))
    elif unavailable:
        print(json.dumps(data, indent=2))
    else:
        print(json.dumps(data.json(), indent=2))


@app.command("gpu", help="Search for a particular GPU by name")
def get_gpu(
    name: Annotated[
        str, typer.Option("--name", "-n", help="Provide the name of the gpu")
    ],
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")
    print(json.dumps(resp.json()["data"][name], indent=2))


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
        print(json.dumps(available_instance, indent=2))
    else:
        print("There are currently no instances available...")

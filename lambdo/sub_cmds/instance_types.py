import json
import typer
from typing_extensions import Annotated
from lambdo.lib.helpers import get_response

app = typer.Typer()


@app.command("all")
def get_available(
        check: Annotated[bool,
        typer.Option("--available/--unavailable",
                     help="Check for availability of gpus")] = True):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")

    if check:
        find_available = [
            inst for inst in resp.json()["data"] if resp.json()["data"][inst]["regions_with_capacity_available"]
        ]

        if not find_available:
            print("There are currently no instances available...")
        else:
            print(json.dumps(find_available, indent=2))
    else:
        find_unavailable = [
            inst for inst in resp.json()["data"] if not resp.json()["data"][inst]["regions_with_capacity_available"]
        ]

        print(json.dumps(find_unavailable, indent=2))

@app.command("gpu")
def get_gpu(name: Annotated[str, typer.Option("--name", "-n", help="Provide the name of the gpu")]):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")
    print(json.dumps(resp.json()["data"][name], indent=2))


@app.command("location")
def get_location(name: Annotated[str, typer.Option("--name", "-n", help="Search by location")]):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")

    find_by_location = [
        loc for inst in resp.json()["data"] for loc in resp.json()["data"][inst]["regions_with_capacity_available"]
        if name.lower() in loc["description"].lower() or name.lower() in loc["name"]
    ]
    if find_by_location:
        available_instance = [
            resp.json()["data"][inst] for inst in resp.json()["data"]
            if find_by_location[0] in resp.json()["data"][inst]["regions_with_capacity_available"]
        ]
        print(json.dumps(available_instance, indent=2))
    else:
        print("There are currently no instances available...")


# if __name__ == "__main__":
#     app()
import json
import typer
import requests
from requests import Response
from typing_extensions import Annotated
from lambdo.lib.settings import api_token


app = typer.Typer()


def main():
    app()


def get_response(url: str) -> Response:
    response = requests.get(
        url=url,
        auth=(api_token, "")
    )

    return response


@app.command()
def instances():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    print(json.dumps(resp.json(), indent=2))


@app.command()
def instance_types(
        available: Annotated[bool, typer.Option(help="Check for availability of gpus")] = False,
        gpu: Annotated[str | None, typer.Option(help="Provide the name of the gpu")] = None,
        by_location: Annotated[str | None, typer.Option(help="Search by location")] = None
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-types | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instance-types")

    if gpu is not None:
        print(json.dumps(resp.json()["data"][gpu], indent=2))
    elif available:
        find_available = [
            inst for inst in resp.json()["data"] if resp.json()["data"][inst]["regions_with_capacity_available"]
        ]
        if find_available:
            print(json.dumps(find_available, indent=2))
        else:
            print("There are currently no instances available...")
    elif by_location is not None:
        find_by_location = [
            loc for inst in resp.json()["data"] for loc in resp.json()["data"][inst]["regions_with_capacity_available"]
            if by_location.lower() in loc["description"].lower() or by_location.lower() in loc["name"]
        ]
        if find_by_location:
            available_instance = [
                resp.json()["data"][inst] for inst in resp.json()["data"]
                if find_by_location[0] in resp.json()["data"][inst]["regions_with_capacity_available"]
            ]
            print(json.dumps(available_instance, indent=2))
        else:
            print("There are currently no instances available...")
    else:
        print(json.dumps(resp.json(), indent=2))


@app.command()
def filesystems():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    main()

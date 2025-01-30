import json
import typer
import click
import requests
# from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from requests import Response

app = typer.Typer()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='allow',
    )


settings = Settings().model_dump()
api_token = settings["api_token"]


def get_response(url: str) -> Response:
    response = requests.get(
        url=url,
        auth=(api_token, "")
    )

    return response


@app.command()
@click.argument("instances")
def instances():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    print(json.dumps(resp.json(), indent=2))


@app.command()
@click.argument("instance-types")
def instance_types(gpu: str | None = None, available: bool = False, by_location: str | None = None):
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
@click.argument("filesystems")
def filesystems():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    app()

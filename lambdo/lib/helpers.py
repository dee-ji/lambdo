import json
import typer
import requests
from requests import Response
from typing import Optional
from lambdo.lib.settings import api_token


# A useful link to Lambda Labs Cloud API Docs: https://cloud.lambdalabs.com/api/v1/docs
def get_response(url: str) -> Response:
    """
    Helper function to get a response
    """
    try:
        response = requests.get(url=url, auth=(api_token, ""))
        response.raise_for_status()
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    return response


def post_request(url: str, data: Optional[dict|None] = None, files: Optional[dict|list|None] = None) -> Response:
    """
    Helper function to post a request
    """
    headers = {"Content-Type": "application/json"}
    try:
        if data is not None:
            data = json.dumps(data)
            response = requests.post(url=url, auth=(api_token, ""), data=data, headers=headers)
            # print(json.dumps(response.json(), indent=2))
        elif files is not None:
            response = requests.post(url=url, auth=(api_token, ""), files=files, headers=headers)
            # print(json.dumps(response.json(), indent=2))
        else:
            response = requests.post(url=url, auth=(api_token, ""), headers=headers)
            # print(json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    response.raise_for_status()

    return response


def delete_request(url: str) -> Response:
    """
    Helper function to delete a resource
    """
    try:
        response = requests.delete(url=url, auth=(api_token, ""))
        response.raise_for_status()
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    return response
import typer
import requests
from requests import Response
from lambdo.lib.settings import api_token


def get_response(url: str) -> Response:
    try:
        response = requests.get(
            url=url,
            auth=(api_token, "")
        )
        response.raise_for_status()
    except requests.RequestException as e:
        typer.echo(f"Error fetching instance types: {e}")
        raise typer.Exit(code=1)

    return response
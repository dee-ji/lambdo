import json
import typer
from lambdo.lib.helpers import get_response
from lambdo.sub_cmds import instance_types


app = typer.Typer()
app.add_typer(instance_types.app, name="instance-types")


def main():
    app()


@app.command()
def instances():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    print(json.dumps(resp.json(), indent=2))


@app.command()
def filesystems():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    print(json.dumps(resp.json(), indent=2))


if __name__ == "__main__":
    main()

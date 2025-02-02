import json
import typer
from lambdo.lib.helpers import get_response
from lambdo.sub_cmds import instance_types


app = typer.Typer(help="Lambdo is a CLI built to utilize Lambda GPU Cloud Public APIs")
app.add_typer(instance_types.app, name="instance-types", help="List the instances types offered by Lambda GPU Cloud")


def main():
    app()


@app.command(help="List your running instances")
def instances():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    print(json.dumps(resp.json(), indent=2))


@app.command(help="List your persistent storage filesystems")
def filesystems():
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/file-systems | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/file-systems")

    print(json.dumps(resp.json(), indent=2))

@app.command(help="Setup the cli with your API KEY")
def setup():
    print("performing setup")


if __name__ == "__main__":
    main()

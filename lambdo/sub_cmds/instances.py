import json
import typer
from typing_extensions import Annotated
from lambdo.lib.helpers import get_response, post_request

app = typer.Typer(invoke_without_command=True)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Display instances from the Lambda Labs Public Cloud API.

    By default, prints all active instances.
    """
    if ctx.invoked_subcommand is not None:
        return
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances | jq .
    resp = get_response(url="https://cloud.lambdalabs.com/api/v1/instances")

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("detail", help="Retrieve the details of an instance")
def get_instance_details(
    inst_id: Annotated[str, typer.Option(help="The id of the instance")],
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instances/INSTANCE-ID | jq .
    resp = get_response(url=f"https://cloud.lambdalabs.com/api/v1/instances/{inst_id}")

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("create", help="Create an instance")
def create_instance(
    region_name: Annotated[str, typer.Option(help="The region name")],
    instance_type_name: Annotated[str, typer.Option(help="The instance type name")],
    ssh_key_names: Annotated[list[str], typer.Option(help="The name of the ssh key")],
    file_system_names: Annotated[
        list[str], typer.Option(help="The name of the filesystem")
    ],
    quantity: Annotated[int, typer.Option(help="The quantity of instances")] = 1,
    name: Annotated[
        str | None, typer.Option(help="The custom name of the instance")
    ] = None,
    from_file: Annotated[
        str | None, typer.Option(help="Path to a file containing required parameters")
    ] = None,
):
    if from_file is not None:
        file = {"file": open(from_file)}
        # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/launch -d @request.json
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/launch",
            files=file,
        )
    else:
        data = {
            "region_name": region_name,
            "instance_type_name": instance_type_name,
            "ssh_key_names": ssh_key_names,
            "file_system_names": file_system_names,
            "quantity": quantity,
            "name": name,
        }
        # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/launch -d @request.json
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/launch",
            data=data,
        )

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("restart", help="Restart instance(s)")
def restart_instances(
    inst_id: Annotated[
        list[str], typer.Option(help="The id of the instance you want to delete")
    ],
):
    data = {"instance_ids": inst_id}
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/restart -d @INSTANCE-IDS
    resp = post_request(
        url="https://cloud.lambdalabs.com/api/v1/instance-operations/restart", data=data
    )

    typer.echo(json.dumps(resp.json(), indent=2))


@app.command("delete", help="Delete instance(s)")
def delete_instances(
    inst_id: Annotated[
        list[str], typer.Option(help="The id of the instance you want to delete")
    ],
    from_file: Annotated[
        str | None, typer.Option(help="Path to a file containing required parameters")
    ] = None,
):
    # curl -u API-KEY: https://cloud.lambdalabs.com/api/v1/instance-operations/terminate -d @INSTANCE-IDS
    if from_file is not None:
        file = {"file": open(from_file)}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            files=file,
        )
    else:
        data = {"instance_ids": inst_id}
        resp = post_request(
            url="https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            data=data,
        )

    typer.echo(json.dumps(resp.json(), indent=2))

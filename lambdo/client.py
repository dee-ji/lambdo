import typer
from lambdo.sub_cmds import (
    filesystems,
    instances,
    instance_types,
    setup,
    ssh_keys,
)


app = typer.Typer(
    help="Lambdo is a CLI tool that utilizes the Lambda GPU Cloud Public APIs",
    no_args_is_help=True,
)
app.add_typer(
    filesystems.app, name="filesystems", help="List your persistent storage filesystems"
)
app.add_typer(
    instances.app, name="instances", help="Manage your Lambda GPU Cloud instances"
)
app.add_typer(
    instance_types.app,
    name="instance-types",
    help="List the instances types offered by Lambda GPU Cloud",
)
app.add_typer(
    setup.app, name="setup", help="Setup Lambdo with your API KEY and SSH path"
)
app.add_typer(ssh_keys.app, name="ssh-keys", help="Manage SSH Keys for your instances")


def main():
    app()


if __name__ == "__main__":
    main()

from typer.testing import CliRunner

from lambdo.sub_cmds.ssh_keys import app

runner = CliRunner()


def test_ssh_keys():
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0


def test_ssh_keys_add():
    result = runner.invoke(app, args=["add", "--help"])
    assert result.exit_code == 0


def test_ssh_keys_delete():
    result = runner.invoke(app, args=["delete", "--help"])
    assert result.exit_code == 0

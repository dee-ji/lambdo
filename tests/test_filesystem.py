from typer.testing import CliRunner

from lambdo.sub_cmds.filesystems import app

runner = CliRunner()


def test_filesystem():
    result = runner.invoke(app, ["-d"])
    assert result.exit_code == 0

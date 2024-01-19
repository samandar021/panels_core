from typer.testing import CliRunner

from typer_cli.main import app

runner = CliRunner()


def test_create_admin_valid_input():
    result = runner.invoke(app, ["create-panel-admin", "test@test.com", "testpassword"])
    assert result.exit_code == 0
    assert "Admin test@test.com created!" in result.output


def test_create_admin_invalid_email():
    result = runner.invoke(app, ["create-panel-admin", "testtest.com", "testpassword"])
    assert result.exit_code == 0
    assert "The email address is not valid." in result.output


def test_create_admin_invalid_password():
    result = runner.invoke(app, ["create-panel-admin", "test@test.com", "short"])
    assert result.exit_code == 0
    assert "Invalid password format" in result.output

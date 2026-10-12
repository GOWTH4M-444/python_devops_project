"""Unit tests for command line interface module."""

from unittest.mock import patch
from app.cli import run


def test_cli_validate_success():
    with patch("app.cli.validate_environment", return_value=True):
        code = run(["validate"])
        assert code == 0


def test_cli_validate_failure():
    with patch("app.cli.validate_environment", return_value=False):
        code = run(["validate"])
        assert code == 1


def test_cli_check_success():
    with patch("app.cli.run_health_checks", return_value=[{"success": True}]):
        code = run(["check"])
        assert code == 0


def test_cli_check_failure():
    with patch("app.cli.run_health_checks", return_value=[{"success": False}]):
        code = run(["check"])
        assert code == 1


def test_cli_report_success():
    with patch("app.cli.generate_report", return_value={"status": "SUCCESS"}):
        code = run(["report"])
        assert code == 0


def test_cli_report_failure():
    with patch("app.cli.generate_report", return_value={"status": "FAILURE"}):
        code = run(["report"])
        assert code == 1


def test_cli_all_workflow_success():
    with patch("app.cli.validate_environment", return_value=True), patch(
        "app.cli.run_health_checks", return_value=[{"success": True}]
    ), patch("app.cli.generate_report", return_value={"status": "SUCCESS"}):
        code = run(["all"])
        assert code == 0


def test_cli_all_workflow_failure():
    with patch("app.cli.validate_environment", return_value=False), patch(
        "app.cli.run_health_checks", return_value=[{"success": False}]
    ), patch("app.cli.generate_report", return_value={"status": "FAILURE"}):
        code = run(["all"])
        assert code == 1


def test_cli_exception_handling():
    with patch(
        "app.cli.validate_environment", side_effect=RuntimeError("Fatal disk error")
    ):
        code = run(["validate"])
        assert code == 1

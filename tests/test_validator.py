"""Unit tests for environment validation module."""

from unittest.mock import patch
from app.validator import validate_environment


def test_validate_environment_returns_boolean():
    result = validate_environment()
    assert isinstance(result, bool)


def test_validate_environment_with_all_vars_present(monkeypatch):
    monkeypatch.setenv("APP_PORT", "5000")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("API_TOKEN", "sample-token")
    monkeypatch.setenv("DB_PASSWORD", "test-password")
    result = validate_environment()
    assert result is True


def test_validate_environment_detects_missing_env_var(monkeypatch):
    monkeypatch.delenv("API_TOKEN", raising=False)
    result = validate_environment()
    assert result is False


def test_validate_environment_detects_missing_file(monkeypatch, tmp_path):
    # Set required env vars
    monkeypatch.setenv("APP_PORT", "5000")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("API_TOKEN", "sample-token")

    # Mock config to require a non-existent file
    mock_config = {
        "required_env_vars": ["APP_PORT"],
        "files_required": [str(tmp_path / "missing_file.txt")],
    }
    with patch("app.validator.load_config", return_value=mock_config):
        result = validate_environment()
        assert result is False

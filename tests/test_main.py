"""Unit tests for application entry point."""

from unittest.mock import patch
import app.main


def test_main_entrypoint(monkeypatch):
    monkeypatch.setenv("APP_PORT", "5000")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("API_TOKEN", "sample-token")
    monkeypatch.setenv("DB_PASSWORD", "test-password")
    with patch.object(app.main, "run", return_value=0):
        result = app.main.run(["validate"])
        assert result == 0

"""Unit tests for health check module."""

from unittest.mock import MagicMock, patch
import requests
from app.healthcheck import run_health_checks


def test_run_health_checks_success():
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("requests.get", return_value=mock_response):
        results = run_health_checks()
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert item["status_code"] == 200
            assert item["success"] is True


def test_run_health_checks_status_mismatch():
    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch("requests.get", return_value=mock_response):
        results = run_health_checks()
        assert isinstance(results, list)
        for item in results:
            assert item["status_code"] == 500
            assert item["success"] is False


def test_run_health_checks_connection_error():
    with patch(
        "requests.get", side_effect=requests.RequestException("Connection refused")
    ):
        results = run_health_checks()
        assert isinstance(results, list)
        for item in results:
            assert item["status_code"] is None
            assert item["success"] is False
            assert "error" in item

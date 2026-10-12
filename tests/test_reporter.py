"""Unit tests for report generator module."""

import json
from unittest.mock import patch
from app.reporter import generate_report


def test_generate_report_creates_files(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_PORT", "5000")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("API_TOKEN", "sample-token")
    monkeypatch.setenv("DB_PASSWORD", "test-password")

    mock_health = [
        {
            "name": "test_service",
            "url": "http://localhost:5000/",
            "status_code": 200,
            "success": True,
        }
    ]

    with patch("app.reporter.run_health_checks", return_value=mock_health):
        reports_dir = str(tmp_path / "reports")
        report = generate_report(reports_dir=reports_dir)

        assert isinstance(report, dict)
        assert report["validation_passed"] is True
        assert report["status"] == "SUCCESS"

        # Check JSON file exists and matches
        json_file = tmp_path / "reports" / "report.json"
        assert json_file.exists()
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data["status"] == "SUCCESS"

        # Check TXT file exists
        txt_file = tmp_path / "reports" / "report.txt"
        assert txt_file.exists()
        content = txt_file.read_text(encoding="utf-8")
        assert "Deployment Environment Report" in content


def test_generate_report_no_health_checks(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_PORT", "5000")
    monkeypatch.setenv("APP_HOST", "127.0.0.1")
    monkeypatch.setenv("API_TOKEN", "sample-token")
    monkeypatch.setenv("DB_PASSWORD", "test-password")

    with patch("app.reporter.run_health_checks", return_value=[]):
        reports_dir = str(tmp_path / "reports_empty")
        report = generate_report(reports_dir=reports_dir)
        assert report["validation_passed"] is True
        txt_file = tmp_path / "reports_empty" / "report.txt"
        assert "No health checks configured." in txt_file.read_text(encoding="utf-8")

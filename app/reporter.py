"""Report generator module writing JSON and formatted text reports."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.healthcheck import run_health_checks
from app.logger import get_logger
from app.validator import validate_environment

logger = get_logger()


def generate_report(
    config_path: str = "configs/config.yaml",
    reports_dir: str = "reports",
    validation_passed: Optional[bool] = None,
    health_checks: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Generate both machine-readable JSON and human-readable text deployment reports.

    Returns:
        dict: The complete report dictionary.
    """
    output_path = Path(reports_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    if validation_passed is None:
        validation_passed = validate_environment(config_path)
    if health_checks is None:
        health_checks = run_health_checks(config_path)

    all_health_passed = (
        all(check.get("success", False) for check in health_checks)
        if health_checks
        else True
    )
    overall_status = (
        "SUCCESS" if (validation_passed and all_health_passed) else "FAILURE"
    )

    report = {
        "timestamp": timestamp,
        "status": overall_status,
        "validation_passed": validation_passed,
        "health_checks": health_checks,
        "summary": {
            "total_health_checks": len(health_checks),
            "passed_health_checks": sum(
                1 for c in health_checks if c.get("success", False)
            ),
            "failed_health_checks": sum(
                1 for c in health_checks if not c.get("success", False)
            ),
        },
    }

    # Write machine-readable JSON report
    json_file = output_path / "report.json"
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)
    logger.info("JSON report generated at %s", json_file)

    # Write human-readable TXT report
    txt_file = output_path / "report.txt"
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write("=" * 60 + "\n")
        file.write("Deployment Environment Report\n")
        file.write("=" * 60 + "\n")
        file.write(f"Generated: {report['timestamp']}\n")
        file.write(f"Overall Status: {report['status']}\n")
        file.write(f"Validation Passed: {report['validation_passed']}\n")
        file.write("-" * 60 + "\n")
        file.write("Health Check Results:\n")
        if not health_checks:
            file.write("  No health checks configured.\n")
        else:
            for check in health_checks:
                status_str = "PASS" if check.get("success") else "FAIL"
                file.write(
                    f"  [{status_str}] {check.get('name')}: "
                    f"URL={check.get('url')} | "
                    f"Status Code={check.get('status_code')} | "
                    f"Expected={check.get('expected_status', 200)}\n"
                )
        file.write("=" * 60 + "\n")
    logger.info("Text report generated at %s", txt_file)

    return report

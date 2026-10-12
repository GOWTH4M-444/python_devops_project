"""Health check module for verifying service endpoints and HTTP statuses."""

from typing import Any, Dict, List
import requests
from app.config import load_config
from app.logger import get_logger

logger = get_logger()


def run_health_checks(config_path: str = "configs/config.yaml") -> List[Dict[str, Any]]:
    """Execute HTTP health checks configured in config.yaml.

    Returns:
        list: A list of dicts with each check's name, url, status_code, and success status.
    """
    config = load_config(config_path)
    results: List[Dict[str, Any]] = []
    timeout = config.get("timeouts", {}).get("request_timeout", 5)

    health_checks = config.get("health_checks", [])
    logger.info("Running %d health check(s)...", len(health_checks))

    for check in health_checks:
        name = check.get("name", "unnamed")
        url = check.get("url", "")
        expected_status = check.get("expected_status", 200)
        method = check.get("method", "GET").upper()
        headers = check.get("headers", {})

        try:
            if method == "POST":
                response = requests.post(url, headers=headers, timeout=timeout)
            else:
                response = requests.get(url, headers=headers, timeout=timeout)

            success = response.status_code == expected_status
            elapsed_ms = (
                round(response.elapsed.total_seconds() * 1000, 2)
                if hasattr(response, "elapsed")
                and hasattr(response.elapsed, "total_seconds")
                else None
            )

            result_entry = {
                "name": name,
                "url": url,
                "status_code": response.status_code,
                "expected_status": expected_status,
                "success": success,
            }
            if elapsed_ms is not None:
                result_entry["response_time_ms"] = elapsed_ms

            results.append(result_entry)
            if success:
                logger.info(
                    "Health check '%s' PASSED (Status: %d%s)",
                    name,
                    response.status_code,
                    f", {elapsed_ms}ms" if elapsed_ms else "",
                )
            else:
                logger.warning(
                    "Health check '%s' FAILED: Expected %d, got %d",
                    name,
                    expected_status,
                    response.status_code,
                )
        except requests.RequestException as exc:
            logger.error("Health check failed for '%s' (%s): %s", name, url, exc)
            results.append(
                {
                    "name": name,
                    "url": url,
                    "status_code": None,
                    "expected_status": expected_status,
                    "success": False,
                    "error": str(exc),
                }
            )

    return results

"""Command-line interface module for Python DevOps Utility."""

import argparse
import sys
from app.healthcheck import run_health_checks
from app.logger import get_logger
from app.reporter import generate_report
from app.validator import validate_environment

logger = get_logger()


def run(argv=None) -> int:
    """Parse command line arguments and execute the corresponding DevOps task.

    Returns:
        int: Exit status code (0 for success, 1 for failure).
    """
    parser = argparse.ArgumentParser(
        description="Python DevOps Utility - Deployment Automation and Environment Health Monitor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=["validate", "check", "report", "all"],
        help=(
            "Command to execute: validate (env vars/files), check (endpoints), "
            "report (generate JSON/TXT), all (complete workflow)"
        ),
    )
    parser.add_argument(
        "--config",
        dest="config_path",
        default="configs/config.yaml",
        help="Path to YAML configuration file (default: configs/config.yaml)",
    )

    args = parser.parse_args(argv)

    try:
        if args.command == "validate":
            is_valid = validate_environment(args.config_path)
            return 0 if is_valid else 1

        elif args.command == "check":
            results = run_health_checks(args.config_path)
            all_passed = (
                all(check.get("success", False) for check in results)
                if results
                else True
            )
            return 0 if all_passed else 1

        elif args.command == "report":
            report = generate_report(args.config_path)
            return 0 if report.get("status") == "SUCCESS" else 1

        elif args.command == "all":
            logger.info("Executing end-to-end DevOps validation workflow...")
            is_valid = validate_environment(args.config_path)
            results = run_health_checks(args.config_path)
            report = generate_report(
                args.config_path,
                validation_passed=is_valid,
                health_checks=results,
            )

            all_health = (
                all(c.get("success", False) for c in results) if results else True
            )
            if is_valid and all_health:
                logger.info(
                    "DevOps workflow completed successfully! [ALL CHECKS PASSED]"
                )
                return 0
            else:
                logger.error(
                    "DevOps workflow encountered failures. Review logs/reports for details."
                )
                return 1

    except Exception as exc:
        logger.error("Error executing command '%s': %s", args.command, exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(run())

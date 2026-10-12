"""Environment validation logic checking required environment variables and files."""

import os
from pathlib import Path
from app.config import load_config
from app.logger import get_logger

logger = get_logger()


def validate_environment(config_path: str = "configs/config.yaml") -> bool:
    """Validate that required environment variables and files are present.

    Returns:
        bool: True if all checks pass, False otherwise.
    """
    config = load_config(config_path)
    passed = True

    logger.info(
        "Starting environment validation for '%s'...",
        config.get("application_name", "app"),
    )

    # Validate required environment variables
    for var in config.get("required_env_vars", []):
        val = os.getenv(var)
        if val is None or val.strip() == "":
            logger.error("Missing environment variable: %s", var)
            passed = False
        else:
            logger.info("Environment variable available: %s", var)

    # Validate required files
    for file_name in config.get("files_required", []):
        if not Path(file_name).exists():
            logger.error("Required file not found: %s", file_name)
            passed = False
        else:
            logger.info("Required file found: %s", file_name)

    if passed:
        logger.info("Environment validation PASSED successfully.")
    else:
        logger.error("Environment validation FAILED.")

    return passed

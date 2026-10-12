"""Configuration loader module for loading YAML configuration and environment variables."""

from pathlib import Path
from typing import Any, Dict
import yaml
from dotenv import load_dotenv

# Automatically load environment variables from root or configs directory
env_root = Path(".env")
env_configs = Path("configs/.env")
if env_root.exists():
    load_dotenv(dotenv_path=env_root)
elif env_configs.exists():
    load_dotenv(dotenv_path=env_configs)
else:
    load_dotenv()


def load_config(path: str = "configs/config.yaml") -> Dict[str, Any]:
    """Load and parse the YAML configuration file."""
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
        return data or {}

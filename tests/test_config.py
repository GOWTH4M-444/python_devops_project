"""Unit tests for configuration loader module."""

import pytest
from app.config import load_config


def test_load_config_returns_dictionary():
    config = load_config()
    assert isinstance(config, dict)


def test_load_config_contains_expected_keys():
    config = load_config()
    assert "environment" in config
    assert "application_name" in config
    assert "required_env_vars" in config
    assert "health_checks" in config
    assert "paths" in config


def test_load_config_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        load_config("non_existent_config.yaml")

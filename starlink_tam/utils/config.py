"""Configuration loading and validation utilities."""

from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import ValidationError

from ..models.config import ModelConfig
from .logger import get_logger

logger = get_logger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_file, "r") as f:
            config_data = yaml.safe_load(f)

        logger.info(f"Loaded configuration from {config_path}")
        return config_data

    except yaml.YAMLError as e:
        logger.error(f"Failed to parse YAML configuration: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise


def validate_config(config_data: Dict[str, Any]) -> ModelConfig:
    """Validate configuration using Pydantic model."""
    try:
        model_config = ModelConfig(**config_data)
        logger.info("Configuration validation successful")
        return model_config

    except ValidationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


def save_config(config: Dict[str, Any], output_path: str) -> None:
    """Save configuration to YAML file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(output_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False, indent=2)

        logger.info(f"Configuration saved to {output_path}")

    except Exception as e:
        logger.error(f"Failed to save configuration: {e}")
        raise

"""Loads and validates application configuration from config/config.json."""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.json"

DEFAULTS = {
    "app_name": "Student Information System",
    "data_file": "data/students.json",
    "log_file": "logs/application.log",
    "max_age": 100,
    "min_age": 1,
}


class ConfigError(Exception):
    """Raised when the configuration is missing or invalid."""


class ConfigManager:
    """Provides configuration values to the rest of the application."""

    def __init__(self, config_path=None):
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        self._config = self._load()

    def _load(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Configuration file is not valid JSON: {exc}")
        except PermissionError:
            raise ConfigError(f"No permission to read configuration: {self.config_path}")
        if not isinstance(loaded, dict):
            raise ConfigError("Configuration must be a JSON object.")
        config = {**DEFAULTS, **loaded}  # missing keys fall back to defaults
        self._validate(config)
        return config

    @staticmethod
    def _validate(config):
        for key in ("app_name", "data_file", "log_file"):
            if not isinstance(config[key], str) or not config[key].strip():
                raise ConfigError(f"'{key}' must be a non-empty string.")
        for key in ("min_age", "max_age"):
            if not isinstance(config[key], int) or isinstance(config[key], bool):
                raise ConfigError(f"'{key}' must be an integer.")
        if config["min_age"] < 0 or config["min_age"] > config["max_age"]:
            raise ConfigError("'min_age' must be >= 0 and not greater than 'max_age'.")

    def get(self, key, default=None):
        return self._config.get(key, default)

    def resolve_path(self, key):
        """Return a path from config, relative to the project root."""
        path = Path(self._config[key])
        return path if path.is_absolute() else PROJECT_ROOT / path

    @property
    def app_name(self):
        return self._config["app_name"]

    @property
    def min_age(self):
        return self._config["min_age"]

    @property
    def max_age(self):
        return self._config["max_age"]

    @property
    def data_file(self):
        return self.resolve_path("data_file")

    @property
    def log_file(self):
        return self.resolve_path("log_file")

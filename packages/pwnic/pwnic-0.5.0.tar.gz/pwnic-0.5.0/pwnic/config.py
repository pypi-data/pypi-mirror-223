from typing import Any

import tomllib

from jsonschema import Draft202012Validator, validate


class _config_class:
    """
    Just a small wrapper so that config['prop'] and config.prop are equivalent
    """

    def __init__(self):
        with open("configs/config.toml", "rb") as fs:
            self._conf = tomllib.load(fs)
        self.schema = {
            "$schema": Draft202012Validator.META_SCHEMA["$id"],
            "type": "object",
            "properties": {
                "starting_timestamp": {"format": "time"},
                "ending_timestamp": {"format": "time"},
                "round_duration": {"type": "number", "exclusiveMinimum": 0},
                "team_id": {
                    "type": "integer",
                    "maximum": self._conf["highest_team_id"],
                    "minimum": 0,
                },
                "highest_team_id": {
                    "type": "integer",
                    "minimum": self._conf["team_id"],
                },
                "base_ip": {
                    "type": "string",
                },
                "exploit_warning_time": {
                    "type": "number",
                    "exclusiveMinimum": 0,
                },
                "submit_url": {"format": "uri"},
                "team_token": {"type": "string"},
                "log_level": {
                    "enum": ["DEBUG", "WARNING", "ERROR", "CRITICAL", "INFO"]
                },
                "flag_regex": {"type": "string", "format": "regex"},
                "timeout": {"type": "number", "exclusiveMinimum": 0},
                "ping_before_exploit": {"type": "boolean"},
            },
        }
        validate(
            self._conf,
            self.schema,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )

    def __getattr__(self, __name: str) -> Any:
        return self._conf[__name]

    def __getitem__(self, __name: str) -> Any:
        return self._conf[__name]


config = _config_class()

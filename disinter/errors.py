from typing import Any, Dict


class APIError(Exception):
    def __init__(self, error: Dict[str, Any]):
        self.error = error


class CommandNameExists(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f"Command: `{name}` already exists")

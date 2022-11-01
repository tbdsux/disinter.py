from typing import Any, Dict


class APIError(Exception):
    def __init__(self, error: Dict[str, Any]):
        self.error = error

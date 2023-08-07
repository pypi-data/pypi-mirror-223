from .jlogr import *

from typing import Optional

__all__ = ["info", "debug", "warning", "error", "parse_list_of_logs"]

def info(message: str) -> None: ...

def debug(message: str) -> None: ...

def warning(message: str) -> None: ...

def error(message: str) -> None: ...

def parse_list_of_logs(
        logs: list[tuple[str, str, Optional[str], Optional[str], Optional[str]]]
        ) -> None: ...

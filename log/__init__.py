
from datetime import datetime


def _print(level: str, message: str) -> None:
    print(f"[{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}] [{level}] {message}")


def info(message: str) -> None:
    _print("INFO", message)


def warn(message: str) -> None:
    _print("WARN", message)


def error(message: str) -> None:
    _print("ERROR", message)


def debug(message: str) -> None:
    _print("DEBUG", message)


def call(command: str, user: str) -> None:
    _print("CALL", f"'{command}' by {user}")


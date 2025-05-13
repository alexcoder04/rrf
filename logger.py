
from datetime import datetime


class Logger:
    def __init__(self, logfile: str) -> None:
        self.logfile = logfile

    def _print(self, level: str, message: str) -> None:
        with open(self.logfile, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}] [{level}] {message}\n")

    def info(self, message: str) -> None:
        self._print("INFO", message)

    def warn(self, message: str) -> None:
        self._print("WARN", message)

    def error(self, message: str) -> None:
        self._print("ERROR", message)

    def debug(self, message: str) -> None:
        self._print("DEBUG", message)

    def call(self, command: str, user: str) -> None:
        self._print("CALL", f"'{command}' by {user}")

    def tail(self, lines: int = 5) -> list:
        with open(self.logfile, "r") as f:
            return f.readlines()[-lines:]


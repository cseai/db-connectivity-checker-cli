"""Minimal console logging for the CLI."""


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def success(msg: str) -> None:
    print(f"[SUCCESS] {msg}")


def error(msg: str) -> None:
    print(f"[ERROR] {msg}")


def result(msg: str) -> None:
    print(f"[RESULT] {msg}")

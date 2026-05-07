"""Loads only the Telegram bot configs."""
import os

from rich import print as rprint
from dotenv import load_dotenv

load_dotenv()

errors = []


def load_or_error(key: str) -> str:
    value = os.environ.get(key)
    if not value:
        errors.append(f"Environment variable [bold red]{key}[/bold red] is not set.")
    return value

TELEGRAM_BOT_TOKEN = load_or_error("TELEGRAM_BOT_TOKEN")

if errors:
    for error in errors:
        rprint(error)
    raise ValueError("Environment variables are not set")
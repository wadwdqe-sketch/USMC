"""Environment-backed Discord bot configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass


def _read_port(value: str | None) -> int:
    """Return a valid TCP port, or the development default."""
    if not value:
        return 8000

    try:
        port = int(value)
    except ValueError as error:
        raise ValueError("PORT must be a number between 1 and 65535") from error

    if not 1 <= port <= 65535:
        raise ValueError("PORT must be a number between 1 and 65535")
    return port


def _read_optional_int(value: str | None) -> int | None:
    """Return an optional positive integer from an environment variable."""
    if not value:
        return None

    try:
        parsed = int(value)
    except ValueError as error:
        raise ValueError("DISCORD_GUILD_ID must be a numeric Discord server ID") from error

    if parsed <= 0:
        raise ValueError("DISCORD_GUILD_ID must be a numeric Discord server ID")
    return parsed


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    host: str = "0.0.0.0"
    port: int = 8000
    app_name: str = "Discord Bot"
    discord_token: str | None = None
    discord_guild_id: int | None = None

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            host=os.getenv("HOST", cls.host),
            port=_read_port(os.getenv("PORT")),
            app_name=os.getenv("APP_NAME", cls.app_name),
            discord_token=os.getenv("DISCORD_TOKEN"),
            discord_guild_id=_read_optional_int(os.getenv("DISCORD_GUILD_ID")),
        )

    def require_discord_token(self) -> str:
        """Return the token or fail with a deployment-friendly message."""
        if not self.discord_token:
            raise RuntimeError(
                "DISCORD_TOKEN is not set. Add your Discord bot token to Railway "
                "Variables before starting the service."
            )
        return self.discord_token
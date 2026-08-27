from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from app.config import Settings


class SettingsTests(unittest.TestCase):
    def test_defaults_are_railway_friendly(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = Settings.from_environment()

        self.assertEqual(settings.host, "0.0.0.0")
        self.assertEqual(settings.port, 8000)
        self.assertIsNone(settings.discord_token)

    def test_token_is_required_before_connecting(self) -> None:
        settings = Settings(discord_token=None)

        with self.assertRaisesRegex(RuntimeError, "DISCORD_TOKEN is not set"):
            settings.require_discord_token()

    def test_token_can_be_loaded_from_environment(self) -> None:
        with patch.dict(
            os.environ,
            {"DISCORD_TOKEN": "test-token", "DISCORD_GUILD_ID": "123456789"},
            clear=True,
        ):
            settings = Settings.from_environment()

        self.assertEqual(settings.require_discord_token(), "test-token")
        self.assertEqual(settings.discord_guild_id, 123456789)


if __name__ == "__main__":
    unittest.main()
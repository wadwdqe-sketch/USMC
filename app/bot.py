"""Discord bot setup and starter commands."""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from .config import Settings
from .health import start_health_server


class BoilerplateBot(commands.Bot):
    """Discord bot with native slash command support."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)

    async def setup_hook(self) -> None:
        """Synchronize slash commands when the bot connects."""
        settings = Settings.from_environment()
        if settings.discord_guild_id is not None:
            guild = discord.Object(id=settings.discord_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Slash commands synced to test server {settings.discord_guild_id}")
            return

        await self.tree.sync()
        print("Slash commands synced globally")

    async def on_ready(self) -> None:
        if self.user is not None:
            print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = BoilerplateBot()


@bot.tree.command(name="ping", description="Check whether the bot is online.")
async def slash_ping(interaction: discord.Interaction) -> None:
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! {latency_ms} ms")


@bot.tree.command(name="hello", description="Get a greeting from the bot.")
async def slash_hello(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


def run_bot() -> None:
    """Start the Railway health endpoint and connect to Discord."""
    settings = Settings.from_environment()
    start_health_server(settings)
    bot.run(settings.require_discord_token())
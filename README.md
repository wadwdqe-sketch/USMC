# Discord Bot Boilerplate

A small Discord bot starter designed to run on Railway. It includes:

- Native Discord slash commands: `/ping` and `/hello`
- A `/health` endpoint for Railway health checks
- Environment-based configuration
- A clear startup error when `DISCORD_TOKEN` is missing

## Discord setup

1. Open the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create an application and open its **Bot** page.
3. Copy the bot token. Keep it private and never commit it to Git.
4. Use the OAuth2 URL generator to invite the bot with the `bot` and
   `applications.commands` scopes. Give it the permissions your commands need.

Once the bot is online, type `/` in a channel where it is installed. Discord
will show `/ping` and `/hello` in its native command picker, just like other
slash-command bots.

For instant command updates while developing, set `DISCORD_GUILD_ID` to the
numeric ID of your test server. Without it, commands sync globally and Discord
may take some time to show new or changed commands.

## Deploy to Railway

1. Create a new Railway service from this project.
2. Add a Railway variable named `DISCORD_TOKEN` containing your bot token.
3. Optionally add `DISCORD_GUILD_ID` with your test server's numeric ID.
4. Railway will install `requirements.txt` and use the `Procfile` start command.
5. Deploy the service.

The bot also starts an HTTP health endpoint on Railway's `PORT` variable. The
endpoint is available at `/health` and returns `{"status":"ok"}`.

## Run locally

```bash
cd python-app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DISCORD_TOKEN="your-token"
python bot.py
```

On Windows PowerShell, use:

```powershell
$env:DISCORD_TOKEN = "your-token"
python bot.py
```

## Test

The configuration tests do not need a Discord token or network access:

```bash
cd python-app
python -m unittest discover -s tests -v
```

## Project structure

```text
python-app/
├── app/
│   ├── bot.py       # Bot class and native slash commands
│   ├── config.py    # Environment-backed settings
│   └── health.py    # Railway health endpoint
├── tests/           # Unit tests
├── bot.py           # Railway entry point
├── requirements.txt # Python dependencies
└── Procfile         # Railway start command
```

To add a command, define a new slash command in `app/bot.py` and restart the
bot so Discord can synchronize it.
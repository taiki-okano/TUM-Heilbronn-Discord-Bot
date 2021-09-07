# TUM Heilbronn Discord Bot

## Before Start

This bot is going to run on Heroku. It can be run for free. You need to create your Heroku account at first.

[Heroku](https://id.heroku.com/login)

After creating your account, you can get the API key for your account. To automatically setup the bot with your Heroku account, you need to set it in GitHub Secrets.

Also, since this is a Discord bot, it requires a token for accessing Discord. You can get it from below.

[Discord Developer Portal](https://discord.com/developers)

## How to Setup (for local debug)

1. Execute `python setup_secrets.py` and type your secrets (e.g. Discord token).

2. Start the bot by executing `python main.py`.

## How to Setup (on Heroku)

1. Add secrets below to GitHub Secrets.

- `DISCORD_TOKEN`
- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `HEROKU_EMAIL`

2. Just push to the repository or manually start GitHub Actions to deploy.

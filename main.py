import discord
import secrets


client = discord.Client()


@client.event
async def on_ready():
    print("The bot has started successfully.")


@client.event
async def on_message(message):
    """
    This specifies how to react to the messages from users.
    """

    # Ignore messages from bots.
    if message.author.bot:
        return

    if message.content == "/test":
        await message.channel.send("Your test has succeeded!!")


client.run(secrets.DISCORD_TOKEN)

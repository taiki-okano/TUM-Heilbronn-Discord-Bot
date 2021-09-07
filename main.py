import discord
import secrets
from email_sender import send_email


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

    message.content = message.content.split()

    if message.content[0] == "/test":
        await message.channel.send("Your test has succeeded!!")

    if message.content[0] == "/mail":
        await send_email(
            to_address=message.content[1],
            subject="TEST",
            body="Hello World",
        )
        await message.channel.send("The email has been sent")

client.run(secrets.DISCORD_TOKEN)

import discord
import secrets
from random import randint
from aiosmtplib.errors import SMTPException
from email_sender import send_email
from registration_mail_template import REGISTRATION_MAIL_TEMPLATE


TUM_STUDENT_ROLE_NAME = "TUM Student"


client = discord.Client()
register_codes = {}


@client.event
async def on_ready():
    print("The bot has started successfully.")


@client.event
async def on_message(message):
    """
    This specifies how to react to the messages from users.
    """

    try:

        # Ignore messages from bots.
        if message.author.bot:
            return

        message.content = message.content.split()

        if message.content[0] == "/test":

            # Email test
            try:
                if message.content[1] == "mail":

                    try:
                        await send_email(
                            to_address=message.content[2],
                            subject="TEST",
                            body="Hello World. This is a test."
                        )
                        await message.channel.send("{} The test mail has been sent.".format(message.author.mention))

                    except SMTPException:
                        await message.channel.send("{} Sending a test mail failed.".format(message.author.mention))

                    except IndexError:
                        await message.channel.send(
                            "{} Specify the email address to send a test mail.".format(message.author.mention)
                        )

            # Default
            except IndexError:
                await message.channel.send("{} Hello World. The bot is running.".format(message.author.mention))

        if message.content[0] == "/register":

            try:

                if message.content[1].isalnum() and not message.content[1].isnumeric():
                    register_code = str(randint(100000, 999999))
                    register_codes[register_code] = message.author

                    try:
                        await send_email(
                            to_address="{}@mytum.de".format(message.content[1]),
                            subject="TUM Heiblronn Discord Server Registration",
                            body=REGISTRATION_MAIL_TEMPLATE.format(
                                username=message.author.name,
                                register_code=register_code,
                            )
                        )

                    except SMTPException:
                        await message.channel.send(
                            "{} Sending a registration mail failed.".format(message.author.mention)
                        )

                    else:
                        await message.channel.send(
                            "{} The registration mail has been sent.".format(message.author.mention)
                        )

                if message.content[1].isnumeric():

                    try:
                        student_role = discord.utils.get(message.guild.roles, name=TUM_STUDENT_ROLE_NAME)

                        await register_codes[message.content[1]].add_roles(student_role)
                        await message.channel.send(
                            "{} The student role is added to your account.".format(message.author.mention)
                        )

                    except KeyError:
                        await message.channel.send(
                            "{} The registration code is invalid.".format(message.author.mention)
                        )

            except IndexError:
                await message.channel.send("{} Invalid command.".format(message.author.mention))

    except Exception:
        await message.channle.send("{} Unknow error happened.".format(message.author.mention))

client.run(secrets.DISCORD_TOKEN)

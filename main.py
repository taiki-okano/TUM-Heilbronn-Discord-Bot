import discord
import secrets
from random import randint
from aiosmtplib.errors import SMTPException
from email_sender import send_email
from registration_mail_template import REGISTRATION_MAIL_TEMPLATE
from welcome_msg_template import WELCOME_MSG_TEMPLATE


TUM_STUDENT_ROLE_NAME = "TUM Student"
GUEST_ROLE_NAME = "Guest"
WELCOME_CHANNEL_NAME = "welcome"
REGISTRATION_CHANNEL_NAME = "registration"
RULES_CHANNEL_NAME = "rules"
SELF_INTRODUCTION_CHANNEL_NAME = "self-introduction"


intents = discord.Intents.all()
client = discord.Client(intents=intents)
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
        if message.author.bot or len(message.content) == 0:
            return

        try:
            # Give Guest role to people who introduce themselves.
            guest_role = discord.utils.get(message.guild.roles, name=GUEST_ROLE_NAME)
            self_introduction_channel = discord.utils.get(message.author.guild.channels, name=SELF_INTRODUCTION_CHANNEL_NAME)

            if message.channel == self_introduction_channel and guest_role not in message.author.roles:
                await message.author.add_roles(guest_role)
        except AttributeError:
            pass

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
                            subject="TUM Heilbronn Discord Server Registration",
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

                elif message.content[1].isnumeric():

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

    except Exception as err:
        await message.channel.send("{} Unknow error happened.".format(message.author.mention))
        print(err)


# Welcome message
@client.event
async def on_member_join(member):

    try:

        if member.bot:
            return

        welcome_channel = discord.utils.get(member.guild.channels, name=WELCOME_CHANNEL_NAME)
        rules_channel = discord.utils.get(member.guild.channels, name=RULES_CHANNEL_NAME)
        registartion_channel = discord.utils.get(member.guild.channels, name=REGISTRATION_CHANNEL_NAME)
        self_introduction_channel = discord.utils.get(member.guild.channels, name=SELF_INTRODUCTION_CHANNEL_NAME)

        await welcome_channel.send(
            WELCOME_MSG_TEMPLATE.format(
                username=member.mention,
                rules_channel=rules_channel.mention,
                registration_channel=registartion_channel.mention,
                self_introduction_channel=self_introduction_channel.mention,
            )
        )

    except Exception as err:
        await member.send("{} Unknow error happened.".format(member.mention))
        print(err)

client.run(secrets.DISCORD_TOKEN)

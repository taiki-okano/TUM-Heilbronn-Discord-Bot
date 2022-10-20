import discord
from discord.ext import commands
from discord.commands import Option
from utils import *
from random import randint
from aiosmtplib.errors import SMTPException


# Bot initialization
tum_bot = commands.Bot(
    intents=discord.Intents.all(),
    status=discord.Status.streaming,
    activity=discord.Activity(
        type=discord.ActivityType.listening, name="I love TUM!")
)

register_codes = []


@tum_bot.event
async def on_ready():
    print(
        f"-----\nLogged in as: {tum_bot.user.name} : {tum_bot.user.id}\n-----\n")


@tum_bot.event
async def on_message(message: discord.Message):
    """
    This specifies how to react to the messages from users.
    """

    # Ignore messages from bots.
    if message.author.bot or len(message.content) == 0:
        return

    try:
        # Give Guest role to people who introduce themselves.
        guest_role = message.guild.get_role(879019868601593926)
        self_introduction_channel = tum_bot.get_channel(879016833976504442)

        if message.channel == self_introduction_channel and guest_role not in message.author.roles:
            await message.author.add_roles(guest_role)
    except Exception as err:
        await message.channel.send(f"Unknown error happened! - {message.author.mention}")
        print(err)


@tum_bot.event
async def on_member_join(member: discord.Member):
    '''
    Greets the user upon joining the server.
    '''

    # Check it's not bot.
    if member.bot:
        return

    try:
        welcome_channel = tum_bot.get_channel(881025666714324992)
        rules_channel = tum_bot.get_channel(879013023107411991)
        registration_channel = tum_bot.get_channel(885063271084855327)
        self_introduction_channel = tum_bot.get_channel(879016833976504442)

        await welcome_channel.send(
            WELCOME_MSG_TEMPLATE.format(
                username=member.mention,
                rules_channel=rules_channel.mention,
                registration_channel=registration_channel.mention,
                self_introduction_channel=self_introduction_channel.mention,
            )
        )

    except Exception as err:
        await member.send("Unknown error happened! {}".format(member.mention))
        print(err)


@tum_bot.slash_command(description="Register new student.", guild_ids=[int(GUILD_ID)])
async def register(
    ctx: discord.ApplicationContext,
    id: Option(str, "Your TUM ID or registration code received via email."),
):
    try:
        if id.isalnum() and not id.isnumeric():
            register_code = str(randint(100000, 999999))
            register_codes.append(register_code)

            try:
                try:
                    await ctx.message.delete()
                except discord.Forbidden:
                    pass

                await send_email(
                    to_address=f"{id}@mytum.de",
                    subject="TUM Heilbronn Discord Server Registration",
                    body=REGISTRATION_MAIL_TEMPLATE.format(
                        username=ctx.author.name, register_code=register_code,)
                )
            except SMTPException:
                await ctx.respond(f"Sending a registration mail failed! - {ctx.author.mention}")
            else:
                await ctx.respond(f"The registration mail has been sent! - {ctx.author.mention}")

        elif id.isnumeric():
            try:
                student_role = ctx.guild.get_role(880770790985957387)
            except AttributeError:
                await ctx.respond(f"You need to do that in the server! - {ctx.author.mention}")
            else:
                if id in register_codes:
                    await ctx.author.add_roles(student_role)
                    register_codes.remove(id)
                    await ctx.respond(f"The student role is added to your account! - {ctx.author.mention}")
                else:
                    await ctx.respond(f"The registration code is invalid! - {ctx.author.mention}")
    except IndexError:
        await ctx.respond(f"Something went wrong! - {ctx.author.mention}")


@tum_bot.slash_command(description="Assign yourself a course role.", guild_ids=[int(GUILD_ID)])
async def course(
    ctx: discord.ApplicationContext,
    course: Option(str, "Course Code.")
):
    try:
        student_role = ctx.guild.get_role(880770790985957387)

        # Check if user already has course role.
        for course_id in COURSE_ROLE_IDS:
            if ctx.guild.get_role(course_id) in ctx.author.roles:
                ctx.respond(
                    f"You've already assigned yourself a course role! - {ctx.author.mention}")
                return

        if student_role in ctx.author.roles:
            course_code_to_role = {}

            for code, role_id in COURSE_CODE_TO_ROLENAME.items():
                course_code_to_role[code] = ctx.guild.get_role(int(role_id))
                await ctx.author.add_roles(course_code_to_role[course])
                await ctx.respond(f"{ctx.author.mention} You are given the `{course_code_to_role[course].name}` role.")
        else:
            await ctx.respond(f"You need to be registered as student to use this command! - {ctx.author.mention}")

    except IndexError:
        await ctx.respond(COURSE_SPECIFICATION_TEMPLATE.format(ctx.author.mention))
    except KeyError:
        await ctx.respond(f"Please specify your course! - {ctx.author.mention}")


@tum_bot.slash_command(description="Test email feature.", guild_ids=[int(GUILD_ID)])
@commands.is_owner()
async def test(
    ctx: discord.ApplicationContext,
    email: Option(str, "Enter valid email address.")
):
    try:
        await send_email(
            to_address=email,
            subject="TEST",
            body="Hello World. This is a test."
        )
        await ctx.respond(f"The test mail has been sent! - {ctx.author.mention}")

    except SMTPException:
        await ctx.respond(f"Sending a test mail failed! - {ctx.author.mention}")
    except IndexError:
        await ctx.respond(f"Specify the email address to send a test mail! - {ctx.author.mention}")


@test.error
async def test_error(ctx: discord.ApplicationContext, error):
    """
        Error handler for test function
    """
    if isinstance(error, commands.CheckFailure):
        await ctx.respond("Hey! You lack permission to use this command as you do not own the bot.")
    else:
        raise error


def activate():
    tum_bot.run(DISCORD_TOKEN)

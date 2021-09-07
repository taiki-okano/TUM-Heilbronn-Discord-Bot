import asyncio
import aiosmtplib
import secrets
from email.message import EmailMessage


async def send_email(
    to_address,
    subject,
    body
):
    """
    Send an email.

    Parameters
    ----------
    to_address: str
    subject: str
    body: str
    """

    message = EmailMessage()
    message["From"] = secrets.SMTP_EMAIL
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(message,
                          hostname=secrets.SMTP_HOSTNAME,
                          username=secrets.SMTP_USER,
                          password=secrets.SMTP_PASSWORD,
                          port=465,
                          use_tls=True)

import os
import json


SECRETS_STORE_PATH = "./.secrets_store.json"

# List of secrets
DISCORD_TOKEN = "GH_SECRETS_DISCORD_TOKEN"
SMTP_EMAIL = "GH_SECRETS_SMTP_EMAIL"
SMTP_HOSTNAME = "GH_SECRETS_SMTP_HOSTNAME"
SMTP_USER = "GH_SECRETS_SMTP_USER"
SMTP_PASSWORD = "GH_SECRETS_SMTP_PASSWORD"


# For local debug
if os.path.exists(SECRETS_STORE_PATH):

    with open(SECRETS_STORE_PATH) as json_file:
        secrets = json.load(json_file)

    for key, value in secrets.items():
        globals()[key] = value

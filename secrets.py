import os
import json


SECRETS_STORE_PATH = "./.secrets_store.json"

# List of secrets
DISCORD_TOKEN = "GH_SECRETS_DISCORD_TOKEN"


# For local debug
if os.path.exists(SECRETS_STORE_PATH):

    with open(SECRETS_STORE_PATH) as json_file:
        secrets = json.load(json_file)

    for key, value in secrets.items():
        globals()[key] = value

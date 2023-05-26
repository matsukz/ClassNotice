import json
from discord_webhook import DiscordWebhook


Webhook_url = ""

loadjson = open(
            "webhook.json",
            "r",
            encoding="utf-8"
        )

impjson = json.load(loadjson)

i = 1

for Message in impjson["Name"][str(i)] == "END":
    Message = impjson["Name"][str(i)]

    webhook = DiscordWebhook(url=Webhook_url,content=Message)

    response = webhook.execute()

    i = i + 1
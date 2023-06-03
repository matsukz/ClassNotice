import json
import datetime
import schedule
import time
from discord_webhook import DiscordWebhook

StopFlag = 0

print("===DAYSTART===")
print(datetime.datetime.now())

NowDate = datetime.date.today()
loadjson = open(
        "Class.json",
        "r",
        encoding="utf-8"
    )

impjson = json.load(loadjson)

Webhook_url = impjson["Webhook"]        

print("DB:IMPJSON")
Week = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

i = 0
while not list(impjson.keys())[i] == Week[NowDate.weekday()]:
    i += 1
Today = list(impjson.keys())[i]
print(Today)

loadjson.close()

ClassNo = 1
StopFlag = 0

def Notice():
    global ClassNo
    global StopFlag
    global impjson
    global Today

    print("===== " + str(ClassNo) + " =====")
    Now = datetime.datetime.now().strftime("%H%M")
    print("NowTime = " + Now)
    try:
        if impjson[Today][str(ClassNo)]["Time"] == "END":
            print("END")
            StopFlag = 1
                
        elif impjson[Today][str(ClassNo)]["Time"] == Now:
            try:
                Message = str(ClassNo) + "限目：" + impjson[Today][str(ClassNo)]["Class"] + " の出席登録が開始されました。"
                Send = DiscordWebhook(url=Webhook_url,content=Message)
                response = Send.execute()
                print("Posted Webhook")
            except Exception as e:
                print("Webhook error!")

            ClassNo += 1

            if impjson[Today][str(ClassNo)]["Time"] == "END":
                Send = DiscordWebhook(url=Webhook_url,content="今日の授業はこれでおしまいです。")
                response = Send.execute()
                StopFlag += 1
            else:
                pass
        else:
            print("NOT MATCH")

    except TypeError:
        print("SKIP NULL")
        ClassNo += 1

schedule.every(1).minutes.do(Notice)

while StopFlag == 0:
    schedule.run_pending()
    time.sleep(1)

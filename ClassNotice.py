import json
import datetime
import schedule
import time
from discord_webhook import DiscordWebhook

StopFlag = 0

Webhook_url = "https://discord.com/api/webhooks/1111462458666786816/Eb3K-BDKSoAORINFyfaBrH8lZDuMMpyG9IEEFYPSSLl9ENeT5OMJg-kI1G6_o3CmPsH4"

def DAY():
    global ClassNo
    global StopFlag
    global impjson
    global Today

    print("===DAYSTART===")
    print(datetime.datetime.now())

    NowDate = datetime.date.today()
    loadjson = open(
            "Class.json",
            "r",
            encoding="utf-8"
        )

    impjson = json.load(loadjson)
            

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
        i = i + 1
    Today = list(impjson.keys())[i]
    print(Today)

    loadjson.close()

    global ClassNo
    ClassNo = 1
    global StopFlag
    StopFlag = 0

DAY()

def CheckTime():
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

            ClassNo = ClassNo + 1

            if impjson[Today][str(ClassNo)]["Time"] == "END":
                Send = DiscordWebhook(url=Webhook_url,content="今日の授業はこれでおしまいです。")
                response = Send.execute()
            else:
                pass  

        else:
            print("NOT MATCH")

    except TypeError:
        print("SKIP NULL")
        ClassNo = ClassNo + 1

schedule.every(1).minutes.do(CheckTime)

while StopFlag == 0:
    schedule.run_pending()
    time.sleep(1)

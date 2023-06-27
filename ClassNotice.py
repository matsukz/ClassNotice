#!/usr/bin/env python3
import json
import datetime
import schedule
import time
from discord_webhook import DiscordWebhook

print("Start:" + str(datetime.datetime.now()))
LoopFlag = True
ERROR = 0

def send(Message):
    global LoopFlag
    try:
        Text = DiscordWebhook(
            url=Webhook_url,
            content=Message
        )
        response = Text.execute()
    except Exception as e:
        print(e)
        LoopFlag = False

def writelog(log):
    try:
        LogName = "CN_" + str(datetime.datetime.now().date()) + ".log"
        Logfile = open(
                # Windows ver
                "log\\" + LogName,
                # UNIX ver
                #"/home/.log"
                "a",
                encoding="utf-8"
        )
        Logfile.write(log)
        Logfile.close()
    except Exception as e:
        print("ログの書き込みに失敗しました")
        print(e)

try:
    log = "\n======DAYSTART======\n"
    log += str(datetime.datetime.now()) + "\n"
    writelog(log)

    try:
        NowDate = datetime.date.today()
        loadjson = open(
                # Windows ver
                "Class.json",
                # UNIX ver
                # /opt/ClassNotice/ClassNotice.json
                "r",
                encoding="utf-8"
        )

        impjson = json.load(loadjson)

        Webhook_url = impjson["Webhook"]

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
        writelog("Today : " + Today + "\n")

        loadjson.close()

    except Exception as e:
        print("Impjson:" + str(e) + "\n")
        writelog("Impjson:" + str(e) + "\n")
        ERROR += 1
        LoopFlag = False

    try: #今日の授業一覧を通知する
        ClassNo = 1
        Message = "本日の授業は\n"
        for item in impjson[Today].values():
            if item["Class"] == "Finish":
                Message += "です。"
            elif item["Class"] == "END":
                Message = Message.rstrip(Message)
            elif item["Class"] is None:
                Message += (str(ClassNo) + "限目：空きコマ\n")
            else:
                Message += (str(ClassNo) + "限目：" + item["Class"] + "（" + item["Room"] + "）\n")
            ClassNo += 1

        send(Message)

    except Exception as e:
        print("Todays_Class:" + str(e) + "\n")
        writelog("Todays_Class:" + str(e) + "\n")
        ERROR += 1
        LoopFlag = False

    NotMatchCount = 0
    ClassNo = 1 #ClassNoは再利用するためリセット

    def notice():
        global impjson, Today
        global ClassNo, NotMatchCount, ERROR
        global LoopFlag
        
        writelog("===== " + str(ClassNo) + " =====\n")
        Now = datetime.datetime.now().strftime("%H%M")
        writelog("NowTime = " + Now + "\n")

        try:
            ClassTime = impjson[Today][str(ClassNo)]["Time"]
            # "Time" == "END" のとき　授業がない
            if ClassTime == "END":
                writelog("Nothing School\n")
                LoopFlag = False

            # "Time" == 現在時(Now)のとき
            elif ClassTime == Now:
                NotMatchCount = 0
                # "Class" is Null
                if impjson[Today][str(ClassNo)]["Class"] is None:
                    writelog("SKIP NULL\n")
                else:
                    try:
                        Message = str(ClassNo) + "限目：" + impjson[Today][str(ClassNo)]["Class"] + " の出席登録が開始されました。"
                        print(Message)
                        send(Message)
                        writelog("Posted Webhook\n")
                    except Exception as e:
                        print("Send_Class" + str(e) +"\n")
                        writelog("Send_Class" + str(e) +"\n")
                        LoopFlag = False
                        ERROR += 1

                # 最後の授業ですか？
                ClassNo += 1

                if impjson[Today][str(ClassNo)]["Class"] == "Finish":
                    send("今日の授業はこれでおしまいです。")
                    LoopFlag = False
                else:
                    pass
            else:
                if NotMatchCount != 150:
                    writelog("Not Match:" + str(NotMatchCount) + "\n")
                    NotMatchCount += 1
                else:
                    writelog("NotMatchCount error!\n")
                    print("NotMatchCount error!\n")
                    ERROR += 1
                    LoopFlag = False

        except Exception as e:
            writelog(str(e) + "\n")
            print(str(e) + "\n")
            ERROR += 1
            LoopFlag = False

    schedule.every(1).minutes.do(notice)

    while LoopFlag == True:
        schedule.run_pending()
        time.sleep(1)

finally:
    log = "ERROR:" + str(ERROR) + "\n"
    log += str(datetime.datetime.now()) + "\n"
    log += "====================\n"
    writelog(log)

print("End:" + str(datetime.datetime.now()))

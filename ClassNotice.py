#!/usr/bin/env python3
import json
import datetime
import schedule
import time
from discord_webhook import DiscordWebhook

print("Start:" + str(datetime.datetime.now()))
LoopFlag = True
ERROR = 0

Logfile = open(
            # Windows ver
            "Log.txt",
            # UNIX ver
            #"/home/.log"
            "a",
            encoding="utf-8"
)

try: #最下部(finally)と繋がっている

    Logfile.write("\n")
    Logfile.write("===DAYSTART===\n")
    Logfile.write(str(datetime.datetime.now()) + "\n")

    try: #Jsonから各種データをロードし変数に格納する。
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
        Logfile.write(Today + "\n")

        loadjson.close()
    except Exception as e:
        print("Impjson:" + str(e) + "\n")
        Logfile.write("Impjson:" + str(e) + "\n")
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

        Send = DiscordWebhook(
            url=Webhook_url,
            content=Message
        )
        response = Send.execute()
    except Exception as e:
        print("Todays_Class:" + str(e) + "\n")
        Logfile.write("Todays_Class:" + str(e) + "\n")
        ERROR += 1
        LoopFlag = False

    NotMatchCount = 0
    ClassNo = 1 #ClassNoは再利用するためリセット

    def Notice():
        global impjson, Today
        global ClassNo, NotMatchCount, ERROR
        global LoopFlag
        
        Logfile.write("===== " + str(ClassNo) + " =====\n")
        Now = datetime.datetime.now().strftime("%H%M")
        Logfile.write("NowTime = " + Now + "\n")

        try:
            ClassTime = impjson[Today][str(ClassNo)]["Time"]
            # "Time" == "END" のとき　授業がない
            if ClassTime == "END":
                Logfile.write("Nothing School\n")
                LoopFlag = False

            # "Time" == 現在時(Now)のとき
            elif ClassTime == Now:
                NotMatchCount = 0
                # "Class" is Null
                if impjson[Today][str(ClassNo)]["Class"] is None:
                    Logfile.write("SKIP NULL\n")
                else:
                    try:
                        Message = str(ClassNo) + "限目：" + impjson[Today][str(ClassNo)]["Class"] + " の出席登録が開始されました。"
                        Send = DiscordWebhook(
                            url=Webhook_url,
                            content=Message
                        )
                        response = Send.execute()
                        Logfile.write("Posted Webhook\n")
                    except Exception as e:
                        print("Send_Class" + str(e) +"\n")
                        Logfile.write("Send_Class" + str(e) +"\n")
                        LoopFlag = False
                        ERROR += 1

                # 最後の授業ですか？
                ClassNo += 1

                if impjson[Today][str(ClassNo)]["Class"] == "Finish":
                    Send = DiscordWebhook(
                        url=Webhook_url,
                        content="今日の授業はこれでおしまいです。"
                    )
                    response = Send.execute()
                    LoopFlag = False
                else:
                    pass

            else:
                if NotMatchCount != 150:
                    Logfile.write("Not Match:" + str(NotMatchCount) + "\n")
                    NotMatchCount += 1
                else:
                    Logfile.write("NotMatchCount error!\n")
                    print("NotMatchCount error!\n")
                    ERROR += 1
                    LoopFlag = False

        except Exception as e:
            Logfile.write(str(e) + "\n")
            print(str(e) + "\n")
            ERROR += 1
            LoopFlag = False

    schedule.every(1).minutes.do(Notice)

    while LoopFlag == True:
        schedule.run_pending()
        time.sleep(1)

finally:
    Logfile.write("ERROR:" + str(ERROR) + "\n")
    Logfile.write(str(datetime.datetime.now()) + "\n")
    Logfile.write("==============\n")
    Logfile.close()

print("End:" + str(datetime.datetime.now()))
